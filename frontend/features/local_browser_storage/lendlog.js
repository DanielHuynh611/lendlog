/* Private account loans and returned history. No browser-local records are uploaded. */
document.addEventListener('DOMContentLoaded', () => {
  'use strict';
  const history = document.body.dataset.view === 'history';
  const form = document.getElementById('loan-form');
  const item = document.getElementById('item-name');
  const borrower = document.getElementById('borrower-name');
  const button = document.getElementById('save-loan');
  const saveError = document.getElementById('save-error');
  const success = document.getElementById('save-status');
  const list = document.getElementById('loan-list');
  const listError = document.getElementById('list-error');
  const retry = document.getElementById('list-retry');
  const more = document.getElementById('show-more');
  const dialog = document.getElementById('record-dialog');
  const actionForm = document.getElementById('record-action-form');
  const actionConfirm = document.getElementById('record-confirm');
  const actionCancel = document.getElementById('record-cancel');
  const actionError = document.getElementById('record-dialog-error');
  const editDialog = document.getElementById('edit-dialog');
  const editForm = document.getElementById('edit-form');
  const editItem = document.getElementById('edit-item-name');
  const editBorrower = document.getElementById('edit-borrower-name');
  const editSave = document.getElementById('edit-save');
  const editCancel = document.getElementById('edit-cancel');
  const editError = document.getElementById('edit-error');
  const listStatus = document.getElementById('list-status');
  let pending = null, editing = null, recordBusy = false;
  let records = [], busy = false, limit = 20, loadVersion = 0;

  async function request(url, options = {}) {
    const response = await fetch(url, {
      credentials: 'same-origin', ...options,
      headers: { 'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content, ...options.headers },
    });
    if (response.status === 401) { location.assign('/login'); throw Error('Please sign in again.'); }
    if (response.status === 204) return null;
    const data = await response.json();
    if (!response.ok) {
      const failure = new Error(data.message || 'The request failed. Please try again.');
      failure.status = response.status;
      failure.fields = data.fields;
      throw failure;
    }
    return data;
  }
  function dateLabel(prefix, timestamp) {
    return prefix + new Intl.DateTimeFormat(undefined, { day: 'numeric', month: 'short', year: 'numeric' }).format(new Date(timestamp));
  }
  function render() {
    const nodes = records.slice(0, limit).map(record => {
      const row = document.createElement('li');
      row.className = 'lend-loan';
      row.dataset.loanId = record.id;
      for (const [label, value] of [['Item', record.item_name], ['Borrower', record.borrower_name]]) {
        const cell = document.createElement('div'), title = document.createElement('small'), text = document.createElement('span');
        title.textContent = label;
        text.textContent = value;
        cell.append(title, text);
        row.append(cell);
      }
      const footer = document.createElement('div');
      footer.className = 'lend-row-actions';
      const date = document.createElement('time');
      date.className = 'lend-row-date';
      date.dateTime = history ? record.returned_at : record.created_at;
      date.textContent = dateLabel(history ? 'Returned ' : 'Lent ', date.dateTime);
      footer.append(date);
      const controls = document.createElement('div');
      controls.className = 'lend-record-buttons';
      for (const [kind, label, classes] of [
        [history ? 'restore' : 'return', history ? 'Mark outstanding' : 'Mark returned', 'z-button--secondary'],
        ['edit', 'Edit', 'z-button--ghost'], ['delete', 'Delete', 'z-button--ghost lend-danger'],
      ]) {
        const action = document.createElement('button');
        action.className = 'z-button ' + classes;
        action.type = 'button';
        action.textContent = label;
        action.dataset.recordAction = kind;
        action.setAttribute('aria-label', kind === 'edit' || kind === 'delete' ? label + ' ' + record.item_name : 'Mark ' + record.item_name + (kind === 'return' ? ' returned' : ' outstanding'));
        action.addEventListener('click', () => {
          if (recordBusy) return;
          if (kind === 'edit') openEdit(record);
          else openAction(record, kind, label);
        });
        controls.append(action);
      }
      footer.append(controls);
      row.append(footer);
      return row;
    });
    list.replaceChildren(...nodes);
    document.getElementById('empty-list').hidden = records.length !== 0;
    document.getElementById('loan-count').textContent = records.length + (records.length === 1 ? ' loan' : ' loans');
    more.hidden = limit >= records.length;
  }
  async function load() {
    const version = ++loadVersion;
    list.setAttribute('aria-busy', 'true');
    listError.hidden = true;
    retry.hidden = true;
    try {
      const result = await request('/api/loans?status=' + (history ? 'returned' : 'active'));
      if (version !== loadVersion) return;
      records = result.loans;
      render();
    } catch (_) {
      if (version !== loadVersion) return;
      listError.textContent = 'Unable to load your loans. Check your connection and try again.';
      listError.hidden = false;
      retry.hidden = false;
      document.getElementById('loan-count').textContent = '';
    } finally {
      if (version === loadVersion) list.setAttribute('aria-busy', 'false');
    }
  }
  function openAction(record, kind, label) {
    if (success) success.hidden = true;
    pending = { record, kind };
    actionError.hidden = true;
    document.getElementById('record-dialog-title').textContent = kind === 'delete' ? 'Delete this loan?' : kind === 'restore' ? 'Mark this loan outstanding again?' : 'Mark this loan returned?';
    document.getElementById('record-dialog-description').textContent = record.item_name + ' — ' + record.borrower_name + '. ' + (kind === 'delete' ? 'This permanently deletes the record. This cannot be undone.' : kind === 'restore' ? 'This moves it from History back to Loans.' : 'This moves the loan to History. You can move it back if needed.');
    actionConfirm.textContent = kind === 'delete' ? 'Delete permanently' : label;
    dialog.showModal();
  }
  function openEdit(record) {
    if (success) success.hidden = true;
    editing = record;
    editItem.value = record.item_name;
    editBorrower.value = record.borrower_name;
    editError.hidden = true;
    for (const [field, id] of [[editItem, 'edit-item-error'], [editBorrower, 'edit-borrower-error']]) {
      field.removeAttribute('aria-invalid');
      document.getElementById(id).hidden = true;
    }
    editDialog.showModal();
    editItem.select();
  }
  function modalBusy(value) {
    recordBusy = value;
    [actionConfirm, actionCancel, editSave, editCancel, editItem, editBorrower].forEach(control => { control.disabled = value; });
    actionForm.setAttribute('aria-busy', String(value));
    editForm.setAttribute('aria-busy', String(value));
  }
  actionCancel.addEventListener('click', () => dialog.close());
  editCancel.addEventListener('click', () => editDialog.close());
  [dialog, editDialog].forEach(modal => modal.addEventListener('cancel', event => { if (recordBusy) event.preventDefault(); }));
  async function finishMutation(record, result, message) {
    if (!result || result.status !== (history ? 'returned' : 'active')) records = records.filter(row => row.id !== record.id);
    else records = records.map(row => row.id === record.id ? result : row);
    render();
    await load();
    listStatus.textContent = message;
    listStatus.hidden = false;
    const target = list.querySelector('[data-loan-id="' + record.id + '"] [data-record-action="edit"]') || list.closest('section');
    if (target.tagName !== 'BUTTON') target.setAttribute('tabindex', '-1');
    target.focus();
  }
  actionForm.addEventListener('submit', async event => {
    event.preventDefault();
    if (!pending || recordBusy) return;
    const { record, kind } = pending;
    modalBusy(true);
    actionError.hidden = true;
    const previousLabel = actionConfirm.textContent;
    actionConfirm.textContent = kind === 'delete' ? 'Deleting…' : 'Updating…';
    try {
      const url = '/api/loans/' + encodeURIComponent(record.id) + (kind === 'delete' ? '' : '/' + kind);
      const result = await request(url, { method: kind === 'delete' ? 'DELETE' : 'POST' });
      dialog.close();
      await finishMutation(record, result, kind === 'delete' ? 'Loan deleted.' : kind === 'restore' ? 'Loan moved back to Loans.' : 'Loan moved to History.');
    } catch (failure) {
      if (failure.status === 404 || failure.status === 409) {
        dialog.close();
        await load();
        listError.textContent = failure.message;
        listError.hidden = false;
      } else {
        actionError.textContent = failure.status ? failure.message : 'Unable to confirm the change. Check your connection and try again, or cancel and refresh to check the record.';
        actionError.hidden = false;
      }
    } finally {
      modalBusy(false);
      actionConfirm.textContent = previousLabel;
    }
  });
  editForm.addEventListener('submit', async event => {
    event.preventDefault();
    if (!editing || recordBusy) return;
    editError.hidden = true;
    const invalidItem = fieldError(editItem, 'edit-item-error', 'an item name');
    const invalidBorrower = fieldError(editBorrower, 'edit-borrower-error', "the borrower's name");
    if (invalidItem || invalidBorrower) {
      editError.textContent = 'Check the highlighted fields.';
      editError.hidden = false;
      (invalidItem ? editItem : editBorrower).focus();
      return;
    }
    const record = editing;
    modalBusy(true);
    editSave.textContent = 'Saving…';
    try {
      const result = await request('/api/loans/' + encodeURIComponent(record.id), {
        method: 'PATCH', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_name: editItem.value.trim(), borrower_name: editBorrower.value.trim() }),
      });
      editDialog.close();
      await finishMutation(record, result, 'Loan details updated.');
    } catch (failure) {
      if (failure.fields?.item_name) fieldError(editItem, 'edit-item-error', 'an item name', failure.fields.item_name);
      if (failure.fields?.borrower_name) fieldError(editBorrower, 'edit-borrower-error', "the borrower's name", failure.fields.borrower_name);
      editError.textContent = failure.status ? failure.message : 'Unable to save changes. Your edits are still here. Check your connection and try again.';
      editError.hidden = false;
    } finally {
      modalBusy(false);
      editSave.textContent = 'Save changes';
    }
  });
  function fieldError(field, id, label, serverMessage) {
    let message = serverMessage || '';
    if (!message && !field.value.trim()) message = 'Enter ' + label + '.';
    else if (!message && [...field.value.trim()].length > 100) message = 'Use no more than 100 characters.';
    const node = document.getElementById(id);
    node.textContent = message;
    node.hidden = !message;
    field.setAttribute('aria-invalid', String(Boolean(message)));
    return message;
  }
  if (form) {
    [item, borrower].forEach(field => field.addEventListener('input', () => {
      if (field.getAttribute('aria-invalid') === 'true') fieldError(field, field === item ? 'item-error' : 'borrower-error', field === item ? 'an item name' : "the borrower's name");
      success.hidden = true;
    }));
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (busy) return;
      success.hidden = true;
      saveError.hidden = true;
      const invalidItem = fieldError(item, 'item-error', 'an item name');
      const invalidBorrower = fieldError(borrower, 'borrower-error', "the borrower's name");
      document.getElementById('validation-status').textContent = [invalidItem, invalidBorrower].filter(Boolean).join(' ');
      if (invalidItem || invalidBorrower) { (invalidItem ? item : borrower).focus(); return; }
      busy = true;
      button.disabled = true;
      button.textContent = 'Saving…';
      item.disabled = borrower.disabled = true;
      const names = { item_name: item.value.trim(), borrower_name: borrower.value.trim() };
      try {
        await request('/api/loans', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(names) });
        form.reset();
        success.textContent = 'Loan saved: ' + names.item_name + ' — ' + names.borrower_name + '.';
        success.hidden = false;
        await load();
      } catch (failure) {
        if (failure.fields) {
          if (failure.fields.item_name) fieldError(item, 'item-error', 'an item name', failure.fields.item_name);
          if (failure.fields.borrower_name) fieldError(borrower, 'borrower-error', "the borrower's name", failure.fields.borrower_name);
        }
        saveError.textContent = failure.status ? failure.message : 'Unable to save. Your text is still here. Check your connection and try again.';
        saveError.hidden = false;
      } finally {
        busy = false;
        button.disabled = false;
        item.disabled = borrower.disabled = false;
        button.textContent = 'Save loan';
        item.focus();
      }
    });
    button.disabled = false;
  }
  more.addEventListener('click', () => { limit += 20; render(); });
  retry.addEventListener('click', load);
  // Refresh from the server when returning from another tab; no personal data is cached locally.
  document.addEventListener('visibilitychange', () => { if (!document.hidden && !busy && !recordBusy && !dialog.open && !editDialog.open) load(); });
  load();
});
