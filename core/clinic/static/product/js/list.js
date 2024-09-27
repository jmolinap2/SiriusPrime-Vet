var tblProducts;
var select_category;
var product = {
    list: function () {
        var parameters = {
            'action': 'search',
            'category': select_category.val(),
        };
        tblProducts = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            columns: [
                {data: "id"},
                {data: "name"},
                {data: "code"},
                {data: "category.name"},
                {data: "type.name"},
                {data: "image"},
                {data: "price"},
                {data: "pvp"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.type.name;
                        switch (row.type.id) {
                            case "product":
                                return '<span class="badge badge-success badge-pill">' + name + '</span>';
                            case "medicine":
                                return '<span class="badge badge-warning badge-pill">' + name + '</span>';
                            case "service":
                                return '<span class="badge badge-primary badge-pill">' + name + '</span>';
                        }
                        return '<span class="badge badge-secondary badge-pill">' + name + '</span>';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<img alt="" src="' + row.image + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.type.id === 'service') {
                            return '<span class="badge badge-secondary badge-pill">Sin stock</span>';
                        }
                        if (row.stock > 0) {
                            return '<span class="badge badge-success badge-pill">' + row.stock + '</span>';
                        }
                        return '<span class="badge badge-danger badge-pill">' + row.stock + '</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a href="' + pathname + 'update/' + row.id + '/" data-toggle="tooltip" title="Editar" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {

    select_category = $('select[name="category"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_category.on('change.select2', function () {
        product.list();
    });

    product.list();
});