var fv;
var tblSearchProducts, tblProducts, tblSearchVaccines, tblVaccines, tblMedicalParameter;
var input_search_products, input_search_vaccines, input_date_joined;
var select_mascot, select_type;
var container_tab;
var sale = {
    detail: {
        products: [],
        vaccines: [],
        subtotal: 0.00,
        iva: 0.00,
        total_iva: 0.00,
        total: 0.00,
    },
    setVisibleTab: function (parameters) {
        parameters.forEach(function (item) {
            var nav = $(container_tab[item.index]);
            var content = $('.tab-content');
            var href = nav.attr('href');
            nav.removeClass('active');
            content.find(href).removeClass('active');
            if (item.visible) {
                nav.closest('li').show();
                if (item.hasOwnProperty('active')) {
                    nav.tab('show');
                }
            } else {
                nav.closest('li').hide();
            }
        });
    },
    calculateInvoice: function () {
        var subtotal = 0.00;
        this.detail.products.forEach(function (value, index, array) {
            value.cant = parseInt(value.cant);
            value.subtotal = value.cant * parseFloat(value.pvp);
            subtotal += value.subtotal;
        });
        this.detail.vaccines.forEach(function (value, index, array) {
            value.cant = parseInt(value.cant);
            value.subtotal = value.cant * parseFloat(value.pvp);
            subtotal += value.subtotal;
        });

        sale.detail.subtotal = subtotal;
        sale.detail.total_iva = sale.detail.subtotal * (sale.detail.iva / 100);
        sale.detail.total = sale.detail.subtotal + sale.detail.total_iva;
        sale.detail.total = parseFloat(sale.detail.total.toFixed(2));

        $('input[name="subtotal"]').val(sale.detail.subtotal.toFixed(2));
        $('input[name="iva"]').val(sale.detail.iva.toFixed(2));
        $('input[name="total_iva"]').val(sale.detail.total_iva.toFixed(2));
        $('input[name="total"]').val(sale.detail.total.toFixed(2));
    },
    addProduct: function (item) {
        this.detail.products.push(item);
        this.listProducts();
    },
    listProducts: function () {
        this.calculateInvoice();
        tblProducts = $('#tblProducts').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.detail.products,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "full_name"},
                {data: "category.name"},
                {data: "stock"},
                {data: "cant"},
                {data: "pvp"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.type.id === 'service') {
                            return '<span class="badge badge-secondary badge-pill">Sin stock</span>';
                        }
                        return '<span class="badge badge-success badge-pill">' + row.stock + '</span>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" autocomplete="off" name="cant" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1, -2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fas fa-times"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                var stock = data.type.id === 'service' ? 1000000 : data.stock;
                tr.find('input[name="cant"]')
                    .TouchSpin({
                        min: 1,
                        max: stock
                    })
                    .on('keypress', function (e) {
                        return validate_text_box({'event': e, 'type': 'numbers'});
                    });
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    getProductsIds: function () {
        return this.detail.products.map(value => value.id);
    },
    listVaccines: function () {
        this.calculateInvoice();
        tblVaccines = $('#tblVaccines').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.detail.vaccines,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "full_name"},
                {data: "id"},
                {data: "date_vaccine"},
                {data: "next_date"},
                {data: "stock"},
                {data: "cant"},
                {data: "pvp"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-7],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="file" accept="image/png,image/jpeg" class="form-control" name="image_vaccine">';
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="date" class="form-control" autocomplete="off" name="date_vaccine" value="' + row.date_vaccine + '">';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="date" class="form-control" autocomplete="off" name="next_date" value="' + row.next_date + '">';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.type.id === 'service') {
                            return '<span class="badge badge-secondary badge-pill">Sin stock</span>';
                        }
                        return '<span class="badge badge-success badge-pill">' + row.stock + '</span>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" autocomplete="off" name="cant" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1, -2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fas fa-times"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                var stock = data.type.id === 'service' ? 1000000 : data.stock;
                tr.find('input[name="cant"]')
                    .TouchSpin({
                        min: 1,
                        max: stock
                    })
                    .on('keypress', function (e) {
                        return validate_text_box({'event': e, 'type': 'numbers'});
                    });
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    getVaccinesIds: function () {
        return this.detail.vaccines.map(value => value.id);
    },
    addVaccine: function (item) {
        this.detail.vaccines.push(item);
        this.listVaccines();
    },
    getMedicalHistory: function () {
        tblMedicalParameter = $('#tblMedicalParameter').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'get_medical_history',
                    'mascot': select_mascot.val()
                },
                dataSrc: ""
            },
            columns: [
                {data: "name"},
                {data: "last_value"},
                {data: "valor"},
                {data: "description"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input class="form-control" autocomplete="off" name="valor" placeholder="Ingrese un valor" value="' + data + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input class="form-control" autocomplete="off" name="description" placeholder="Ingrese una descripción" value="' + data + '" maxlength="500">';
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

document.addEventListener('DOMContentLoaded', function (e) {
    fv = FormValidation.formValidation(document.getElementById('frmForm'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                // excluded: new FormValidation.plugins.Excluded(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                mascot: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una mascota'
                        },
                    }
                },
                date_joined: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    }
                },
                type: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un tipo de venta'
                        },
                    }
                },
                symptoms: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                diagnosis: {
                    validators: {
                        notEmpty: {},
                    }
                },
                observation: {
                    validators: {
                        notEmpty: {},
                    }
                },
            },
        }
    )
        .on('core.form.invalid', function () {
            $('a[href="#home"][data-toggle="tab"]').parent().find('i').removeClass().addClass('fas fa-times');
        })
        .on('core.element.validated', function (e) {
            var container = $(e.element).parent().parent();
            if (container.hasClass('tab-pane')) {
                var tab = e.element.closest('.tab-pane'), tabId = tab.getAttribute('id');
                if (e.valid) {
                    $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i').removeClass();
                } else {
                    $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i').removeClass().addClass('fas fa-times');
                }
            }
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            var container = $(e.element).parent().parent();
            if (container.hasClass('tab-pane')) {
                var tab = e.element.closest('.tab-pane'), tabId = tab.getAttribute('id');
                if (e.valid) {
                    $('a[href="#' + tabId + '"][data-toggle="tab"]').parent().find('i').removeClass();
                }
            }
            if (!e.result.valid) {
                const messages = [].slice.call(fv.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var params = new FormData(fv.form);
            params.append('medical_parameter', JSON.stringify(tblMedicalParameter.rows().data().toArray()));
            params.append('products', JSON.stringify(sale.detail.products));
            params.append('vaccines', JSON.stringify(sale.detail.vaccines));
            var list_url = $(fv.form).attr('data-url');
            var args = {
                'params': params,
                'success': function (request) {
                    dialog_action({
                        'content': '¿Desea Imprimir el Comprobante?',
                        'success': function () {
                            window.open(request.print_url, '_blank');
                            location.href = list_url;
                        },
                        'cancel': function () {
                            location.href = list_url;
                        }
                    });
                }
            };
            submit_with_formdata(args);
        });
});

$(function () {
    input_date_joined = $('input[name="date_joined"]');
    input_search_vaccines = $('input[name="search_vaccines"]')
    input_search_products = $('input[name="search_products"]')
    select_mascot = $('select[name="mascot"]');
    select_type = $('select[name="type"]');
    container_tab = $('.nav-tabs a');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    select_mascot
        .select2({
            theme: "bootstrap4",
            language: 'es',
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                url: pathname,
                data: function (params) {
                    return {
                        term: params.term,
                        action: 'search_mascot'
                    };
                },
                processResults: function (data) {
                    return {
                        results: data
                    };
                },
            },
            placeholder: 'Ingrese una descripción',
            minimumInputLength: 1,
        })
        .on('select2:select', function (e) {
            sale.getMedicalHistory();
            fv.revalidateField('mascot');
        })
        .on('select2:clear', function (e) {
            sale.getMedicalHistory();
            fv.revalidateField('mascot');
        });

    // Products

    $('.btnRemoveAllProducts').on('click', function () {
        if (sale.detail.products.length === 0) return false;
        dialog_action({
            'content': '¿Estas seguro de eliminar todos los items de tu detalle?',
            'success': function () {
                sale.detail.products = [];
                sale.listProducts();
            },
            'cancel': function () {

            }
        });
    });

    input_search_products.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_products',
                    'term': request.term,
                    'ids': JSON.stringify(sale.getProductsIds()),
                },
                dataType: "json",
                type: "POST",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            ui.item.cant = 1;
            sale.addProduct(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearProducts').on('click', function () {
        input_search_products.val('').focus();
    });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_products',
                    'term': input_search_products.val(),
                    'ids': JSON.stringify(sale.getProductsIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "full_name"},
                {data: "type.name"},
                {data: "price"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.type.name;
                        switch (row.type.id) {
                            case "product":
                                return '<span class="badge badge-success badge-pill">' + name + '</span>';
                            case "medicine":
                                return '<span class="badge badge-success badge-pill">' + name + '</span>';
                            case "service":
                                return '<span class="badge badge-primary badge-pill">' + name + '</span>';
                        }
                        return '<span class="badge badge-secondary badge-pill">' + name + '</span>';
                    }
                },
                {
                    targets: [-3],
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
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                    }
                }
            ],
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            var row = tblSearchProducts.row(tr.row).data();
            row.cant = 1;
            sale.addProduct(row);
            tblSearchProducts.row(tr.row).remove().draw();
        });

    $('#tblProducts tbody')
        .off()
        .on('change', 'input[name="cant"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            sale.detail.products[tr.row].cant = parseInt($(this).val());
            sale.calculateInvoice();
            $('td:last', tblProducts.row(tr.row).node()).html('$' + sale.detail.products[tr.row].subtotal.toFixed(2));
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            sale.detail.products.splice(tr.row, 1);
            tblProducts.row(tr.row).remove().draw();
            sale.calculateInvoice();
        });

    // Vaccines

    $('.btnRemoveAllVaccines').on('click', function () {
        if (sale.detail.vaccines.length === 0) return false;
        dialog_action({
            'content': '¿Estas seguro de eliminar todos los items de tu detalle?',
            'success': function () {
                sale.detail.vaccines = [];
                sale.listVaccines();
            },
            'cancel': function () {

            }
        });
    });

    input_search_vaccines.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_vaccines',
                    'term': request.term,
                    'ids': JSON.stringify(sale.getVaccinesIds()),
                },
                dataType: "json",
                type: "POST",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            ui.item.cant = 1;
            sale.addVaccine(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearVaccines').on('click', function () {
        input_search_vaccines.val('').focus();
    });

    $('.btnSearchVaccines').on('click', function () {
        tblSearchVaccines = $('#tblSearchVaccines').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_vaccines',
                    'term': input_search_vaccines.val(),
                    'ids': JSON.stringify(sale.getVaccinesIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "full_name"},
                {data: "type.name"},
                {data: "price"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.type.name;
                        switch (row.type.id) {
                            case "product":
                                return '<span class="badge badge-success badge-pill">' + name + '</span>';
                            case "medicine":
                                return '<span class="badge badge-success badge-pill">' + name + '</span>';
                            case "service":
                                return '<span class="badge badge-primary badge-pill">' + name + '</span>';
                        }
                        return '<span class="badge badge-secondary badge-pill">' + name + '</span>';
                    }
                },
                {
                    targets: [-3],
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
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                    }
                }
            ],
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalSearchVaccines').modal('show');
    });

    $('#tblSearchVaccines tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var tr = tblSearchVaccines.cell($(this).closest('td, li')).index();
            var row = tblSearchVaccines.row(tr.row).data();
            row.cant = 1;
            sale.addVaccine(row);
            tblSearchVaccines.row(tr.row).remove().draw();
        });

    $('#tblVaccines tbody')
        .off()
        .on('change', 'input[name="image_vaccine"]', function () {
            var tr = tblVaccines.cell($(this).closest('td, li')).index();
            var reader = new FileReader();
            reader.readAsDataURL(this.files[0]);
            reader.onload = function () {
                sale.detail.vaccines[tr.row].image_vaccine = reader.result;
            };
            reader.onerror = function (error) {
                console.log('Error: ', error);
            };
        })
        .on('change', 'input[name="cant"]', function () {
            var tr = tblVaccines.cell($(this).closest('td, li')).index();
            sale.detail.vaccines[tr.row].cant = parseInt($(this).val());
            sale.calculateInvoice();
            $('td:last', tblVaccines.row(tr.row).node()).html('$' + sale.detail.vaccines[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="date_vaccine"]', function () {
            var tr = tblVaccines.cell($(this).closest('td, li')).index();
            sale.detail.vaccines[tr.row].date_vaccine = $(this).val();
        })
        .on('change', 'input[name="next_date"]', function () {
            var tr = tblVaccines.cell($(this).closest('td, li')).index();
            sale.detail.vaccines[tr.row].next_date = $(this).val();
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblVaccines.cell($(this).closest('td, li')).index();
            sale.detail.vaccines.splice(tr.row, 1);
            tblVaccines.row(tr.row).remove().draw();
            sale.calculateInvoice();
        });

    $('.btnHistoryMedicines').on('click', function () {
        var mascot = select_mascot.val();
        if ($.isEmptyObject(mascot)) {
            message_error('Seleccione una mascota');
            return false;
        }
        $('#tblMedicinesHistory').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_medicines_history',
                    'mascot': mascot
                },
                dataSrc: ""
            },
            columns: [
                {data: "date_vaccine"},
                {data: "product.name"},
                {data: "product.category.name"},
                {data: "next_date"},
            ],
            columnDefs: [
                {
                    targets: [-1, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
            ],
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalMedicinesHistory').modal('show');
    });

    // Medical History

    $('.btnSearchMedicalHistory').on('click', function () {
        var mascot = select_mascot.val();
        if ($.isEmptyObject(mascot)) {
            message_error('Seleccione una mascota');
            return false;
        }
        $('#tblMedicalHistory').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_medical_history',
                    'mascot': mascot,
                },
                dataSrc: ""
            },
            columnDefs: [
                {
                    targets: '_all',
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
            ],
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalMedicalHistory').modal('show');
    });

    // Form

    input_date_joined.datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false
    });

    input_date_joined.on('change.datetimepicker', function (e) {
        fv.revalidateField('date_joined');
    });

    select_type.on('change', function () {
        var id = $(this).val();
        var fields = ['symptoms', 'diagnosis', 'observation'];
        fv.validateField('type').then(function (status) {
            if (status === 'Valid') {
                if (id === 'sale') {
                    sale.setVisibleTab([
                        {'index': 0, 'visible': false},
                        {'index': 1, 'visible': true, 'active': true},
                        {'index': 2, 'visible': false},
                        {'index': 3, 'visible': false}
                    ]);
                    fields.forEach(function (value, index, array) {
                        fv.disableValidator(value);
                    });
                } else {
                    sale.setVisibleTab(
                        [
                            {'index': 0, 'visible': true, 'active': true},
                            {'index': 1, 'visible': true},
                            {'index': 2, 'visible': true},
                            {'index': 3, 'visible': true}
                        ]);
                    fields.forEach(function (value, index, array) {
                        fv.enableValidator(value);
                    });
                }
            }
        });
    });

    $('#tblMedicalParameter tbody')
        .off()
        .on('change', 'input[name="valor"]', function () {
            var tr = tblMedicalParameter.cell($(this).closest('td, li')).index();
            row = tblMedicalParameter.row(tr.row).data();
            row.valor = $(this).val();
        })
        .on('keyup', 'input[name="description"]', function () {
            var tr = tblMedicalParameter.cell($(this).closest('td, li')).index();
            row = tblMedicalParameter.row(tr.row).data();
            row.description = $(this).val();
        });

    // Init

    sale.setVisibleTab(
        [
            {'index': 0, 'visible': false},
            {'index': 1, 'visible': false},
            {'index': 2, 'visible': false},
            {'index': 3, 'visible': false}
        ]
    );

    sale.getMedicalHistory();

    if (!$.isEmptyObject(select_type.val())) {
        select_type.trigger('change');
        return false;
    }
});