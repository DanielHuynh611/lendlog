/* The visible MVP is browser-local: no loan names are sent to the server. */
document.addEventListener('DOMContentLoaded', () => {
  'use strict';
  const key = 'lendlog:loans:v1';
  const form = document.getElementById('loan-form');
  const item = document.getElementById('item-name');
  const borrower = document.getElementById('borrower-name');
  const button = document.getElementById('save-loan');
  const storageError = document.getElementById('storage-error');
  const success = document.getElementById('save-status');
  const list = document.getElementById('loan-list');
  let busy = false;

  function validName(value) { return typeof value === 'string' && value.trim().length > 0 && [...value.trim()].length <= 100; }
  function read() {
    const raw = localStorage.getItem(key);
    const records = raw === null ? [] : JSON.parse(raw);
    if (!Array.isArray(records) || records.some(row => !row || typeof row.id !== 'string' || !validName(row.item_name) || !validName(row.borrower_name) || !Number.isFinite(Date.parse(row.created_at)))) {
      throw Error('Stored data is not in the expected format.');
    }
    return records;
  }
  function storageFailure() {
    storageError.textContent = 'Unable to access or save browser storage. Your entered text is unchanged. Check browser storage permissions or available space; existing records have not been overwritten.';
    storageError.hidden = false;
  }
  function render(records) {
    const nodes = records.slice().reverse().map(record => {
      const row = document.createElement('li');
      row.className = 'lend-loan';
      for (const [label, value] of [['Item', record.item_name], ['Borrower', record.borrower_name]]) {
        const cell = document.createElement('div');
        const title = document.createElement('small');
        title.textContent = label;
        const text = document.createElement('span');
        text.textContent = value;
        cell.append(title, text);
        row.append(cell);
      }
      return row;
    });
    list.replaceChildren(...nodes);
    document.getElementById('empty-list').hidden = records.length !== 0;
    document.getElementById('loan-count').textContent = `${records.length} ${records.length === 1 ? 'loan' : 'loans'}`;
  }
  function fieldError(field, id, label) {
    let message = '';
    if (!field.value.trim()) message = `Enter ${label}.`;
    else if ([...field.value.trim()].length > 100) message = 'Use no more than 100 characters.';
    const node = document.getElementById(id);
    node.textContent = message;
    node.hidden = !message;
    field.setAttribute('aria-invalid', String(Boolean(message)));
    return message;
  }
  [item, borrower].forEach(field => field.addEventListener('input', () => {
    if (field.getAttribute('aria-invalid') === 'true') fieldError(field, field === item ? 'item-error' : 'borrower-error', field === item ? 'an item name' : "the borrower's name");
    success.hidden = true;
  }));
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy) return;
    success.hidden = true;
    const invalidItem = fieldError(item, 'item-error', 'an item name');
    const invalidBorrower = fieldError(borrower, 'borrower-error', "the borrower's name");
    document.getElementById('validation-status').textContent = [invalidItem, invalidBorrower].filter(Boolean).join(' ');
    if (invalidItem || invalidBorrower) { (invalidItem ? item : borrower).focus(); return; }
    busy = true;
    button.disabled = true;
    button.textContent = 'Saving…';
    form.setAttribute('aria-busy', 'true');
    const names = { item_name: item.value.trim(), borrower_name: borrower.value.trim() };
    async function save() {
      const records = read();
      const record = { id: crypto.randomUUID(), ...names, created_at: new Date().toISOString() };
      localStorage.setItem(key, JSON.stringify([...records, record]));
      render([...records, record]);
    }
    try {
      // Coordinate writes between tabs where supported; duplicates remain valid loans.
      if (navigator.locks?.request) await navigator.locks.request('lendlog-save', save);
      else await save();
      form.reset();
      storageError.hidden = true;
      success.textContent = `Loan saved: ${names.item_name} — ${names.borrower_name}.`;
      success.hidden = false;
      item.focus();
    } catch (_) { storageFailure(); }
    finally {
      busy = false;
      button.disabled = false;
      button.textContent = 'Save loan';
      form.setAttribute('aria-busy', 'false');
    }
  });
  window.addEventListener('storage', event => {
    if (event.key === key || event.key === null) {
      try { render(read()); storageError.hidden = true; }
      catch (_) { storageFailure(); }
    }
  });
  try { render(read()); }
  catch (_) { storageFailure(); }
  // A subsequent save can retry storage without losing the user's draft.
  button.disabled = false;
});
