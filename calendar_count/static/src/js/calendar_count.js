odoo.define('calendar_count.CalendarRenderer', function(require) {
    "use strict";
    var CalendarRenderer = require('web.CalendarRenderer');

    CalendarRenderer.include({
        _renderCount: function(){
            var self = this;
            $('[id^="count_"]').remove()

            var getDaysArray = function(start, end) {
                for (var arr = [], dt = new Date(start); dt < end; dt.setDate(dt.getDate() + 1)) {
                    arr.push(new Date(dt));
                }
                if (!end)
                    arr.push(new Date(start));
                return arr;
            };

            // Loop every event
            for (let i = 0; i < self.state.data.length; i++) {
                let listDates = getDaysArray(self.state.data[i].r_start, self.state.data[i].r_end);

                // List date for increment count
                for (let i = 0; i < listDates.length; i++) {

                    let dateStr = moment(listDates[i]).format("YYYY-MM-DD");
                    let id = 'count_' + dateStr;
                    let cell = $('td[data-date="' + dateStr + '"]')

                    if (cell.length > 1)
                        if ($('#' + id).length) {
                            let nextVal = Number($('#' + id).text().replace('(', '').replace(')', '')) + 1;
                            let html = '<span id="' + id + '"class="fc-day-number" style="color:red">(' + nextVal + ')</span>';
                            if (cell.hasClass('fc-today'))
                                html = '<span id="' + id + '"class="fc-day-number" style="color:red;background-color:transparent !important">(' + nextVal + ')</span>';
                            $('#' + id).replaceWith(html)
                        } else {
                            let html = '<span id="' + id + '"class="fc-day-number" style="color:red">(1)</span>';
                            if (cell.hasClass('fc-today'))
                                html = '<span id="' + id + '"class="fc-day-number" style="color:red;background-color:transparent !important">(1)</span>';
                            $(html).appendTo($(cell[1]))
                        }

                }
            }
        },

        _getFullCalendarOptions: function(fcOptions) {
            var self = this;
            let res = this._super.apply(this, arguments);
            return Object.assign(res, {
                events: async function (info, successCB) {
                    await successCB(self.state.data);
                    setTimeout(() => self._renderCount(), 1000);
                },

            })
        }
    });
});