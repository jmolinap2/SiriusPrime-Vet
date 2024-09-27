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
            columns: [
                {data: "date_vaccine"},
                {data: "sale.mascot.client.user.names"},
                {data: "sale.mascot.name"},
                {data: "sale.mascot.breed_pet.type_pet.name"},
                {data: "sale.mascot.breed_pet.name"},
                {data: "product.name"},
                {data: "product.category.name"},
                {data: "next_date"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-left',
                    render: function (data, type, row) {
                        return '<a class="text-success" href="' + row.vaccine_image + '" target="_blank">' + row.product.name + '</a>';
                    }
                },
                {
                    targets: [0, -1],
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