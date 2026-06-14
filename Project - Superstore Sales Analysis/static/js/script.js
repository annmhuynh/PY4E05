function resetFilters() {
    document.getElementById("start-date").value = "{{ min_date }}";
    document.getElementById("end-date").value = "{{ max_date }}";
    document.getElementById("region").value = "";
    document.getElementById("segment").value = "";
    document.getElementById("category").value = "";
    document.forms[0].submit();
}