function goToFromTable(elem) {
    console.log(elem.closest('.table-row-clickable'));
    tr = elem.closest('.table-row-clickable')
    url = tr.getAttribute('href');
    location.href = url;
}