var firstSeatLabel = 1;
var selectedContainer = [];
var sc;

$(document).ready(function () {

    sc = $('#seat-map').seatCharts({
            map: [
                'cccccccc',
                'cccccccc',
                'cccccccc',
                'cccccccc',
                'cccccccc',
                'cccccccc',
                'cccccccc',
                'cccccccc',
                'cccccccc',
                'cccccccc',
                'cccccccc',
                'cccccccc',
                'cccccccc',
                'cccccccc',
                'cccccccc',
            ],

            seats: {
                c: {
                    classes: 'std-class', //your custom CSS class
                    category: 'Standard Class'
                }
            },

            naming: {
                top: false,
                getLabel: function (character, row, column) {
                    return firstSeatLabel++;
                },
            },

            legend: {
                node: $('#legend'),
                items: [
                    ['c', 'available', 'Available'],
                    ['f', 'unavailable', 'Already Booked']
                ]
            },

            click: function () {
                if (this.status() == 'available') {
                    selectedContainer.push(this.settings.id);
                    handleFreightFareForm2();
                    return 'selected';

                } else if (this.status() == 'selected') {
                    selectedContainer.splice(selectedContainer.indexOf(this.settings.id), 1);
                    handleFreightFareForm2();
                    return 'available';

                } else if (this.status() == 'unavailable') {
                    return 'unavailable';
                } else {
                    return this.style();
                }
            }

        });
});
