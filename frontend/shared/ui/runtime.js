/* Application behavior for the versioned component catalogue. No generated JavaScript. */
(() => {
  'use strict';
  const all = (selector, root = document) => [...root.querySelectorAll(selector)];
  const at = (value, path) => !path ? value : path.split('.').reduce((v, key) => v != null && typeof v === 'object' ? v[key] : undefined, value);
  const display = value => value == null ? '—' : typeof value === 'object' ? JSON.stringify(value) : String(value);
  const formatted = (value, format) => {
    if (value == null) return '—';
    if (format === 'boolean') return value ? 'Yes' : 'No';
    if (format === 'percent') return `${value}%`;
    if (format === 'date' || format === 'datetime') {
      const date = new Date(value);
      return Number.isNaN(date.getTime()) ? display(value) : format === 'date' ? date.toLocaleDateString() : date.toLocaleString();
    }
    return display(value);
  };
  const names = route => [...route.matchAll(/\{([A-Za-z_]\w*)\}/g)].map(match => match[1]);
  function materialize(route, values) {
    if (!route.startsWith('/') || route.startsWith('//') || /[\\\s?#<>]/.test(route)) throw Error('Invalid destination.');
    return route.replace(/\{([A-Za-z_]\w*)\}/g, (_, key) => {
      if (values[key] == null || values[key] === '') throw Error(`Missing ${key.replaceAll('_', ' ')}. Open a record first.`);
      return encodeURIComponent(values[key]);
    });
  }
  function routeValues(route) {
    const keys = names(route);
    const pattern = '^' + route.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/\\\{[A-Za-z_]\w*\\\}/g, '([^/]+)') + '/?$';
    const match = (window.__ZORENTIA_PREVIEW_ROUTE__ || location.pathname).match(new RegExp(pattern));
    return Object.fromEntries(keys.map((key, i) => [key, match ? decodeURIComponent(match[i + 1]) : window.__ZORENTIA_PREVIEW__ ? 'example-id' : undefined]));
  }
  function validate(value, schema, label) {
    const type = schema.type;
    if (type === 'object') {
      if (!value || typeof value !== 'object' || Array.isArray(value)) throw Error(`${label} must be an object.`);
      for (const key of schema.required || []) if (value[key] === undefined || value[key] === '') throw Error(`${label}: ${key} is required.`);
      for (const [key, child] of Object.entries(value)) {
        if (schema.properties?.[key]) validate(child, schema.properties[key], key);
        else if (schema.additionalProperties === false) throw Error(`${label}: unexpected ${key}.`);
      }
    } else if (type === 'array') {
      if (!Array.isArray(value)) throw Error(`${label} must be a list.`);
      if (value.length < (schema.minItems ?? 0) || value.length > (schema.maxItems ?? Infinity)) throw Error(`${label} has an invalid number of items.`);
      if (schema.uniqueItems && new Set(value.map(item => JSON.stringify(item))).size !== value.length) throw Error(`${label} must contain unique items.`);
      value.forEach(item => validate(item, schema.items || {}, label));
    } else if (type === 'integer' || type === 'number') {
      if (typeof value !== 'number' || !Number.isFinite(value) || type === 'integer' && !Number.isInteger(value)) throw Error(`${label} must be a valid ${type}.`);
      if (value < (schema.minimum ?? -Infinity) || value > (schema.maximum ?? Infinity) || value <= (schema.exclusiveMinimum ?? -Infinity) || value >= (schema.exclusiveMaximum ?? Infinity)) throw Error(`${label} is outside the allowed range.`);
      if (schema.multipleOf && Math.abs(value / schema.multipleOf - Math.round(value / schema.multipleOf)) > 1e-8) throw Error(`${label} has an invalid increment.`);
    } else if (type === 'boolean' && typeof value !== 'boolean') throw Error(`${label} must be true or false.`);
    else if (type === 'string') {
      if (typeof value !== 'string' || value.length < (schema.minLength ?? 0) || value.length > (schema.maxLength ?? Infinity)) throw Error(`${label} has an invalid length.`);
      if (schema.pattern && !new RegExp(schema.pattern).test(value)) throw Error(`${label} has an invalid format.`);
    }
    if (schema.enum && !schema.enum.some(item => JSON.stringify(item) === JSON.stringify(value))) throw Error(`${label} is not an allowed choice.`);
  }
  function formValues(form, schema) {
    const values = {};
    if (!form) return values;
    for (const input of all('[name]', form)) {
      const rules = schema.properties?.[input.name];
      if (!rules || input.disabled) continue;
      let value = input.type === 'checkbox' ? input.checked : input.value;
      if (value === '' && !(schema.required || []).includes(input.name)) continue;
      if (rules.type === 'integer' || rules.type === 'number') value = value === '' ? NaN : Number(value);
      if (rules.type === 'object' || rules.type === 'array') {
        try { value = JSON.parse(value); } catch { throw Error(`${input.name.replaceAll('_', ' ')} must contain valid JSON.`); }
      }
      if (rules.type === 'boolean' && input.type !== 'checkbox') value = value === 'true';
      if (input.type === 'datetime-local' && value) value = new Date(value).toISOString();
      validate(value, rules, input.name.replaceAll('_', ' '));
      Object.defineProperty(values, input.name, { value, enumerable: true, configurable: true });
    }
    return values;
  }
  function mount(config) {
    if (config.application_id) { window.__ZORENTIA_APPLICATION__ = config.application_id; window.__ZORENTIA_WORKFLOW_VERSION__ = config.workflow_version; }
    const start = async () => {
      if (config.application_id && window.__ZORENTIA_PREVIEW__ && window.parent !== window) {
        await new Promise(resolve => {
          const timer = setTimeout(() => { window.removeEventListener('message', receive); resolve(); }, 1000);
          function receive(event) {
            if (event.source !== window.parent || event.data?.type !== 'frontend-preview:state' || event.data.application_id !== config.application_id || event.data.workflow_version !== config.workflow_version) return;
            window.__ZORENTIA_PREVIEW_STATE__ = event.data.state || {};
            window.__ZORENTIA_PREVIEW_ROUTE__ = event.data.route;
            clearTimeout(timer); window.removeEventListener('message', receive); resolve();
          }
          window.addEventListener('message', receive);
          window.parent.postMessage({ type: 'frontend-preview:ready', application_id: config.application_id, workflow_version: config.workflow_version }, '*');
        });
      }
      const actions = new Map(config.actions.map(action => [action.id, action]));
      const parameters = routeValues(config.screen_route);
      const tableState = new WeakMap();
      const disabledBefore = new WeakMap();
      const storage = window.Zui.storage;
      const responses = new Map(), itemRecords = new WeakMap(), queuedReads = new WeakSet(), workflow = Object.create(null);
      const stateDefinitions = new Map((config.state || []).map(state => [state.name, state]));
      const stateKey = `zorentia-workflow:${config.application_id}:${config.workflow_version}`;
      let saved = window.__ZORENTIA_PREVIEW_STATE__ || {};
      if (!window.__ZORENTIA_PREVIEW__ && config.application_id) {
        try { saved = JSON.parse(sessionStorage.getItem(stateKey) || '{}'); } catch { saved = {}; }
      }
      if (!saved || typeof saved !== 'object' || Array.isArray(saved)) saved = {};
      const availableState = new Set((Array.isArray(saved.__available) ? saved.__available : []).filter(name => stateDefinitions.has(name)));
      for (const state of stateDefinitions.values()) {
        const schema = { type: state.type, ...(state.type === 'array' ? { items: { type: 'string' }, maxItems: 100 } : {}) };
        try { validate(saved[state.name], schema, state.name); workflow[state.name] = saved[state.name]; }
        catch { workflow[state.name] = structuredClone(state.initial); availableState.delete(state.name); }
      }
      function persist() {
        if (!stateDefinitions.size) return;
        const snapshot = { ...workflow, __available: [...availableState] };
        if (window.__ZORENTIA_PREVIEW__) {
          window.__ZORENTIA_PREVIEW_STATE__ = snapshot;
          window.parent.postMessage({ type: 'frontend-preview:workflow', application_id: config.application_id, workflow_version: config.workflow_version, state: snapshot }, '*');
        } else if (config.application_id) {
          try { sessionStorage.setItem(stateKey, JSON.stringify(snapshot)); }
          catch { throw Error('Browser session storage is unavailable. This workflow cannot survive navigation.'); }
        }
      }
      function setState(name, value) {
        const state = stateDefinitions.get(name);
        if (!state) throw Error('Unknown workflow state.');
        validate(value, { type: state.type, ...(state.type === 'array' ? { items: { type: 'string' }, maxItems: 100 } : {}) }, name);
        workflow[name] = value;
        availableState.add(name);
      }
      function boundValues(bindings, item) {
        const result = {};
        for (const binding of bindings || []) {
          const value = binding.source === 'literal' ? binding.value : binding.source === 'state' ? availableState.has(binding.path) ? workflow[binding.path] : undefined
            : binding.source === 'route' ? parameters[binding.path] : binding.source === 'item' ? at(item, binding.path)
            : at(responses.get(binding.action_id), binding.path);
          Object.defineProperty(result, binding.name, { value, enumerable: true });
        }
        return result;
      }
      function navigate(route) {
        persist();
        if (window.__ZORENTIA_PREVIEW__) window.parent.postMessage({ type: 'frontend-preview:navigate', route, application_id: config.application_id, workflow_version: config.workflow_version, state: { ...workflow, __available: [...availableState] } }, '*');
        else location.assign(route);
      }
      function updatePresentation() {
        all('[data-when]').forEach(node => {
          const rules = JSON.parse(node.dataset.when);
          node.hidden = !availableState.has(rules.state) || JSON.stringify(workflow[rules.state]) !== JSON.stringify(rules.equals);
        });
        all('[data-progress-state]').forEach(node => {
          if (node.dataset.totalState) {
            const total = workflow[node.dataset.totalState];
            node.parentElement.hidden = !availableState.has(node.dataset.totalState) || typeof total !== 'number' || total < 1;
            if (!node.parentElement.hidden) node.max = total;
          }
          node.value = Math.min(Number(node.max), Math.max(0, Number(workflow[node.dataset.progressState]) || 0));
          node.parentElement.querySelector('[data-progress-status]').textContent = `${node.value} of ${node.max}`;
        });
        all('[data-state-details]').forEach(node => {
          const fields = all('[data-state-value]', node);
          node.hidden = fields.some(field => !availableState.has(field.dataset.stateValue));
          fields.forEach(field => { field.textContent = formatted(workflow[field.dataset.stateValue], field.dataset.format); });
        });
        all('[data-choices-config]').forEach(node => {
          const rules = JSON.parse(node.dataset.choicesConfig), selected = workflow[rules.state];
          all('[data-choice-value]', node).forEach(button => {
            const active = rules.multiple ? selected?.includes(button.dataset.choiceValue) : selected === button.dataset.choiceValue;
            button.setAttribute('aria-pressed', String(Boolean(active)));
            button.classList.toggle('z-button--primary', Boolean(active)); button.classList.toggle('z-button--secondary', !active);
          });
        });
        links(document, parameters);
      }
      function drawChoices(node, payload) {
        const rules = JSON.parse(node.dataset.choicesConfig);
        const options = rules.options || at(payload, rules.path);
        if (!Array.isArray(options)) throw Error('The options response did not contain the expected list.');
        const buttons = options.map(option => {
          const value = rules.options ? option.value : at(option, rules.value_path), label = rules.options ? option.label : at(option, rules.label_path);
          if (typeof value !== 'string' || typeof label !== 'string') throw Error('An option is missing its value or label.');
          const button = document.createElement('button'); button.type = 'button'; button.className = 'z-button z-button--secondary';
          button.dataset.choiceValue = value; button.textContent = label; button.setAttribute('aria-pressed', 'false');
          return button;
        });
        node.querySelector('[data-choice-options]').replaceChildren(...buttons);
        node.querySelector('[data-choice-empty]').hidden = options.length !== 0;
        updatePresentation();
      }
      const region = (root, kind) => root.querySelector(`[data-${kind}-region]`);
      function show(root, kind, message) {
        const node = region(root, kind); if (!node) { if (config.application_id && kind === 'error') window.Zui.toast(message); return; }
        node.hidden = false; node.textContent = message;
        if (kind === 'error') node.focus();
      }
      function busy(root, state) {
        root.setAttribute('aria-busy', String(state));
        const indicator = region(root, 'loading'); if (indicator) indicator.hidden = !state;
        all('button,input,textarea,select', root).forEach(node => {
          if (state) { disabledBefore.set(node, node.disabled); node.disabled = true; }
          else if (disabledBefore.has(node)) { node.disabled = disabledBefore.get(node); disabledBefore.delete(node); }
        });
      }
      function links(scope, values) {
        all('[data-screen-link]', scope).forEach(link => {
          try {
            if (JSON.parse(link.dataset.requiresState || '[]').some(name => !availableState.has(name) || workflow[name] === '' || workflow[name] == null || Array.isArray(workflow[name]) && !workflow[name].length)) throw Error('Complete the selection first.');
            link.href = materialize(link.dataset.screenLink, { ...values, ...boundValues(JSON.parse(link.dataset.linkInputs || '[]')) }); link.removeAttribute('aria-disabled');
          }
          catch { link.removeAttribute('href'); link.setAttribute('aria-disabled', 'true'); }
        });
      }
      links(document, parameters);
      function drawTable(node) {
        const state = tableState.get(node), options = JSON.parse(node.dataset.tableConfig);
        const { records, page, size } = state;
        const rows = records.slice(page * size, (page + 1) * size).map(record => {
          const row = node.querySelector('template').content.cloneNode(true);
          all('[data-value]', row).forEach(cell => { cell.textContent = formatted(at(record, cell.dataset.value), cell.dataset.format); });
          const link = row.querySelector('[data-row-link]');
          if (link) {
            const values = { ...parameters, ...record };
            const missing = names(options.row_route).filter(key => values[key] == null);
            if (missing.length === 1) values[missing[0]] = at(record, options.row_key || 'id');
            try { link.href = materialize(options.row_route, values); }
            catch { link.removeAttribute('href'); link.setAttribute('aria-disabled', 'true'); }
          }
          return row;
        });
        node.querySelector('tbody').replaceChildren(...rows);
        node.querySelector('[data-empty]').hidden = records.length !== 0;
        node.querySelector('[data-page-status]').textContent = records.length ? `${page * size + 1}–${Math.min((page + 1) * size, records.length)} of ${records.length} loaded records` : '0 records';
        node.querySelector('[data-page="-1"]').disabled = page === 0;
        node.querySelector('[data-page="1"]').disabled = (page + 1) * size >= records.length;
      }
      function render(root, payload) {
        all('[data-collection-config]', root).forEach(node => {
          const options = JSON.parse(node.dataset.collectionConfig), records = at(payload, options.path);
          if (!Array.isArray(records)) throw Error('The response did not contain the expected records.');
          const rows = records.map(record => {
            const row = node.querySelector('template').content.cloneNode(true);
            all('[data-item-value]', row).forEach(cell => { cell.textContent = display(at(record, cell.dataset.itemValue)); });
            all('[data-item-action]', row).forEach(button => itemRecords.set(button, record));
            const link = row.querySelector('[data-item-link]');
            if (link) {
              const values = { ...parameters, ...record }, missing = names(options.row_route).filter(key => values[key] == null);
              if (missing.length === 1) values[missing[0]] = at(record, options.key_path);
              link.href = materialize(options.row_route, values);
            }
            return row;
          });
          node.querySelector('[data-items]').replaceChildren(...rows);
          node.querySelector('[data-empty]').hidden = records.length !== 0;
        });
        all('[data-choices-config]', root).forEach(node => drawChoices(node, payload));
        all('[data-table-config]', root).forEach(node => {
          const options = JSON.parse(node.dataset.tableConfig), records = at(payload, options.path);
          if (!Array.isArray(records)) throw Error('The response did not contain the expected records.');
          tableState.set(node, { records: [...records], page: 0, size: options.page_size || 20, sort: null, direction: 1 });
          drawTable(node);
        });
        all('[data-value]', root).filter(node => !node.closest('[data-table-config]')).forEach(node => {
          const details = node.closest('[data-details-path]');
          node.textContent = formatted(at(details ? at(payload, details.dataset.detailsPath) : payload, node.dataset.value), node.dataset.format);
        });
      }
      all('[data-table-config]').forEach(node => {
        node.addEventListener('click', event => {
          const state = tableState.get(node); if (!state) return;
          const page = event.target.closest('[data-page]'), sort = event.target.closest('[data-column-sort]');
          if (page) state.page += Number(page.dataset.page);
          if (sort) {
            const key = sort.dataset.columnSort;
            state.direction = state.sort === key ? -state.direction : 1; state.sort = key; state.page = 0;
            state.records.sort((a, b) => String(at(a, key) ?? '').localeCompare(String(at(b, key) ?? ''), undefined, { numeric: true }) * state.direction);
            all('th', node).forEach(th => th.removeAttribute('aria-sort'));
            sort.closest('th').setAttribute('aria-sort', state.direction === 1 ? 'ascending' : 'descending');
          }
          if (page || sort) drawTable(node);
        });
      });
      async function request(action, values) {
        const schema = action.request_schema || {};
        validate(Object.fromEntries(Object.entries(values).filter(([key]) => Object.hasOwn(schema.properties || {}, key))), { ...schema, type: 'object' }, 'Request');
        const pathNames = names(action.route);
        const url = materialize(action.route, values);
        const data = Object.fromEntries(Object.entries(values).filter(([key]) => !pathNames.includes(key) && Object.hasOwn(schema.properties || {}, key)));
        const headers = { Accept: 'application/json' }, token = storage.get(config.storage_key);
        if (action.authentication === 'required' && !token && !window.__ZORENTIA_PREVIEW__) throw Error('Please sign in before using this action.');
        if (token) headers.Authorization = `Bearer ${token}`;
        const options = { method: action.method, headers, credentials: 'same-origin' };
        let target = url;
        if (['GET', 'HEAD'].includes(action.method)) {
          const query = new URLSearchParams();
          for (const [key, value] of Object.entries(data)) query.set(key, typeof value === 'object' ? JSON.stringify(value) : String(value));
          if (query.size) target += '?' + query;
        } else { headers['Content-Type'] = 'application/json'; options.body = JSON.stringify(data); }
        const response = await fetch(target, options);
        const payload = response.status === 204 || action.method === 'HEAD' ? {} : await response.json().catch(() => { throw Error('The server returned an unreadable response.'); });
        if (!response.ok) throw Error(typeof payload.message === 'string' ? payload.message : typeof payload.error === 'string' ? payload.error : `Request failed (${response.status}).`);
        return payload;
      }
      async function execute(root, action, prefill = false, item = null) {
        if (root.getAttribute('aria-busy') === 'true') { if (config.application_id && ['GET', 'HEAD'].includes(action.method)) queuedReads.add(root); return; }
        try {
          for (const kind of ['error', 'success']) { const node = region(root, kind); if (node) node.hidden = true; }
          const form = prefill ? null : root.tagName === 'FORM' ? root : root.querySelector('form');
          if (form && !form.reportValidity()) return;
          const values = { ...parameters, ...formValues(form, action.request_schema || {}), ...boundValues(action.inputs, item) };
          for (const binding of action.inputs || []) {
            const type = action.request_schema?.properties?.[binding.name]?.type;
            if (binding.source === 'route' && ['integer', 'number'].includes(type) && values[binding.name] !== undefined) values[binding.name] = Number(values[binding.name]);
          }
          if (config.application_id && root.dataset.autoload === 'true' && !form?.matches(':focus-within') &&
              [...(action.request_schema?.required || []), ...names(action.route)].some(key => values[key] === undefined || values[key] === '')) {
            if (action.inputs?.some(binding => ['state', 'response'].includes(binding.source) && (values[binding.name] === '' || values[binding.name] == null))) {
              show(root, 'error', 'Complete the previous step before loading this page.');
              const message = region(root, 'error');
              if (message && config.entry_route) {
                const link = document.createElement('a'); link.className = 'z-button z-button--secondary'; link.textContent = 'Start again'; link.href = config.entry_route; link.dataset.screenLink = config.entry_route; link.dataset.resetState = JSON.stringify([...stateDefinitions.keys()]); message.append(link);
              }
            }
            return;
          }
          busy(root, true);
          const bindingSignature = JSON.stringify(boundValues(action.inputs, item));
          const payload = await request(action, values);
          if (config.application_id && ['GET', 'HEAD'].includes(action.method) && bindingSignature !== JSON.stringify(boundValues(action.inputs, item))) { queuedReads.add(root); return; }
          if (config.application_id) validate(payload, action.response_schema || {}, 'Response');
          responses.set(action.id, payload);
          if (prefill) {
            const record = at(payload, root.dataset.prefillPath || '');
            all('[name]', root).forEach(input => {
              if (!record || !Object.hasOwn(record, input.name) || /password|secret|token/i.test(input.name)) return;
              if (input.type === 'checkbox') input.checked = Boolean(record[input.name]);
              else if (input.type === 'datetime-local') input.value = String(record[input.name]).slice(0, 16);
              else input.value = typeof record[input.name] === 'object' ? JSON.stringify(record[input.name], null, 2) : record[input.name] ?? '';
            });
          } else {
            if (action.token_path && !window.__ZORENTIA_PREVIEW__) {
              const token = at(payload, action.token_path);
              if (typeof token !== 'string' || !token) throw Error('The sign-in response did not contain the expected access token.');
              if (!window.__ZORENTIA_PREVIEW__ && !storage.set(config.storage_key, token)) throw Error('Browser storage is unavailable. Sign-in could not be retained.');
            }
            render(root, payload);
            for (const node of all('[data-result-action]').filter(node => node.dataset.resultAction === action.id)) {
              node.hidden = false; render(node, payload);
            }
            for (const update of action.state_updates || []) setState(update.state, at(payload, update.path));
            if (config.application_id) { persist(); updatePresentation(); }
            show(root, 'success', ['GET', 'HEAD'].includes(action.method) ? 'Loaded.' : action.token_path ? 'Signed in.' : 'Changes saved.');
            for (const target of action.reload_action_ids || []) {
              const owner = all('[data-action-id]').find(node => node.dataset.actionId === target);
              if (owner) await execute(owner, actions.get(target));
            }
            for (const owner of all('[data-action-id][data-autoload="true"]')) {
              const dependent = actions.get(owner.dataset.actionId);
              if (dependent?.inputs?.some(binding => binding.source === 'response' && binding.action_id === action.id)) await execute(owner, dependent);
            }
            if (action.success_route && (config.application_id || !window.__ZORENTIA_PREVIEW__)) navigate(materialize(action.success_route, { ...values, ...payload }));
          }
        } catch (error) { show(root, 'error', error.message || 'Something went wrong. Please try again.'); }
        finally {
          busy(root, false);
          // Pagination is computed from the new response, independently of action loading.
          all('[data-table-config]', root).forEach(node => { if (tableState.has(node)) drawTable(node); });
          if (queuedReads.has(root)) { queuedReads.delete(root); await execute(root, action, prefill, item); }
        }
      }
      all('[data-action-id]').forEach(root => {
        const action = actions.get(root.dataset.actionId); if (!action) return;
        root.addEventListener('submit', event => { event.preventDefault(); execute(root, action); });
        root.querySelector('[data-reload]')?.addEventListener('click', () => execute(root, action));
        if (root.dataset.prefillAction) execute(root, actions.get(root.dataset.prefillAction), true);
        else if (root.dataset.autoload === 'true') execute(root, action);
      });
      if (config.application_id) {
        all('[data-choices-config]').forEach(node => {
          const options = JSON.parse(node.dataset.choicesConfig);
          if (options.options) drawChoices(node, null);
          node.addEventListener('click', event => {
            const button = event.target.closest('[data-choice-value]'); if (!button) return;
            const selected = workflow[options.state];
            try {
              setState(options.state, options.multiple ? selected.includes(button.dataset.choiceValue)
                ? selected.filter(value => value !== button.dataset.choiceValue) : [...selected, button.dataset.choiceValue] : button.dataset.choiceValue);
              persist(); updatePresentation();
            } catch (error) { show(node.closest('[data-action-id]') || node, 'error', error.message); return; }
            all('[data-action-id][data-autoload="true"]').forEach(owner => {
              const action = actions.get(owner.dataset.actionId);
              if (action?.inputs?.some(binding => binding.source === 'state' && binding.path === options.state)) execute(owner, action);
            });
          });
        });
        document.addEventListener('click', event => {
          const itemButton = event.target.closest('[data-item-action]');
          if (itemButton) { event.preventDefault(); execute(itemButton.parentElement, actions.get(itemButton.dataset.itemAction), false, itemRecords.get(itemButton)); return; }
          const link = event.target.closest('[data-screen-link]');
          if (!link) return;
          if (link.getAttribute('aria-disabled') === 'true') { event.preventDefault(); return; }
          event.preventDefault();
          try {
            const route = materialize(link.dataset.screenLink, { ...parameters, ...boundValues(JSON.parse(link.dataset.linkInputs || '[]')) });
            for (const name of JSON.parse(link.dataset.resetState || '[]')) { setState(name, structuredClone(stateDefinitions.get(name).initial)); availableState.delete(name); }
            navigate(route);
          } catch (error) { window.Zui.toast(error.message); }
        }, true);
        updatePresentation();
      }
      all('[data-options-action]').forEach(select => {
        const form = select.closest('form'), action = actions.get(select.dataset.optionsAction);
        if (!form || !action) return;
        (async () => {
          try {
            busy(form, true);
            const payload = await request(action, parameters);
            const records = at(payload, select.dataset.optionsPath || '');
            if (!Array.isArray(records)) throw Error('The options response did not contain the expected list.');
            const choices = records.map(record => {
              const value = at(record, select.dataset.optionValuePath);
              const label = at(record, select.dataset.optionLabelPath);
              if (value == null || label == null) throw Error('An option was missing its value or label.');
              const option = document.createElement('option');
              option.value = String(value); option.textContent = String(label);
              return option;
            });
            const placeholder = document.createElement('option');
            placeholder.value = ''; placeholder.textContent = 'Choose…';
            select.replaceChildren(placeholder, ...choices);
          } catch (error) {
            select.replaceChildren(Object.assign(document.createElement('option'), { value: '', textContent: 'Options unavailable' }));
            show(form, 'error', error.message || 'Options could not be loaded.');
          } finally { busy(form, false); }
        })();
      });
      all('[data-tabs]').forEach(group => {
        const tabs = all('[role=tab]', group).filter(tab => tab.closest('[data-tabs]') === group);
        function activate(tab, focus = false) {
          tabs.forEach(item => {
            const active = item === tab; item.setAttribute('aria-selected', String(active)); item.tabIndex = active ? 0 : -1;
            document.getElementById(item.getAttribute('aria-controls')).hidden = !active;
          });
          if (focus) tab.focus();
        }
        tabs.forEach((tab, index) => {
          tab.addEventListener('click', () => activate(tab));
          tab.addEventListener('keydown', event => {
            const next = event.key === 'ArrowRight' ? (index + 1) % tabs.length : event.key === 'ArrowLeft' ? (index + tabs.length - 1) % tabs.length : event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : null;
            if (next !== null) { event.preventDefault(); activate(tabs[next], true); }
          });
        });
        if (tabs.length) activate(tabs[0]);
      });
    };
    if (document.readyState === 'complete') start();
    else document.addEventListener('DOMContentLoaded', start, { once: true });
  }
  window.ZorentiaUI = { mount };
})();
