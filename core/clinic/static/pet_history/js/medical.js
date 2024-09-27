var select_mascot;
var pet_history = {
    list: function () {
        $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search',
                    'mascot': select_mascot.val()
                },
                dataSrc: ""
            },
            columnDefs: [
                {
                    targets: ['_all'],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    select_mascot = $('select[name="mascot"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_mascot.on('change', function () {
        pet_history.list();
    });

    pet_history.list();
});