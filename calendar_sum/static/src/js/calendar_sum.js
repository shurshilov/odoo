openerp.calendar_sum = function(instance) {
    var _t = instance.web._t,
        QWeb = instance.web.qweb;

        function get_fc_defaultOptions() {
        shortTimeformat = Date.CultureInfo.formatPatterns.shortTime;
        var dateFormat = Date.normalizeFormat(instance.web.strip_raw_chars(_t.database.parameters.date_format));
        return {
            weekNumberTitle: _t("W"),
            allDayText: _t("All day"),
            buttonText : {
                today:    _t("Today"),
                month:    _t("Month"),
                week:     _t("Week"),
                day:      _t("Day")
            },
            monthNames: Date.CultureInfo.monthNames,
            monthNamesShort: Date.CultureInfo.abbreviatedMonthNames,
            dayNames: Date.CultureInfo.dayNames,
            dayNamesShort: Date.CultureInfo.abbreviatedDayNames,
            firstDay: Date.CultureInfo.firstDayOfWeek,
            weekNumbers: true,
            axisFormat : shortTimeformat.replace(/:mm/,'(:mm)'),
            timeFormat : {
               // for agendaWeek and agendaDay               
               agenda: shortTimeformat + '{ - ' + shortTimeformat + '}', // 5:00 - 6:30
                // for all other views
                '': shortTimeformat.replace(/:mm/,'(:mm)')  // 7pm
            },
            titleFormat: {
                month: 'MMMM yyyy',
                week: dateFormat + "{ '&#8212;'"+ dateFormat,
                day: dateFormat,
            },
            columnFormat: {
                month: 'ddd',
                week: 'ddd ' + dateFormat,
                day: 'dddd ' + dateFormat,
            },
            weekMode : 'liquid',
            aspectRatio: 1.8,
            snapMinutes: 15,
        };
    }

   instance.web_calendar.CalendarView.include({

            get_fc_init_options: function () {
/*                            var self = this;
            this._super.apply(this, arguments);*/
            //Documentation here : http://arshaw.com/fullcalendar/docs/
            var self = this;
            return  $.extend({}, get_fc_defaultOptions(), {
                
                defaultView: (this.mode == "month")?"month":
                    (this.mode == "week"?"agendaWeek":
                     (this.mode == "day"?"agendaDay":"month")),
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'month,agendaWeek,agendaDay,azino'
                },
                selectable: !this.options.read_only_mode && this.create_right,
                selectHelper: true,
                editable: !this.options.read_only_mode,
                droppable: true,

                // callbacks

                eventDrop: function (event, _day_delta, _minute_delta, _all_day, _revertFunc) {
                    var data = self.get_event_data(event);
                    self.proxy('update_record')(event._id, data); // we don't revert the event, but update it.
                },
                eventResize: function (event, _day_delta, _minute_delta, _revertFunc) {
                    var data = self.get_event_data(event);
                    self.proxy('update_record')(event._id, data);
                },
                eventRender: function (event, element, view) {
                    element.find('.fc-event-title').html(event.title + event.attendee_avatars);
                    //MY
                    var model = new instance.web.Model(self.model);
                    //console.log(self.fields_view.arch.attrs.sum)
                    if (!self.fields_view.arch.attrs.sum)
                        return
                    var field = self.fields_view.arch.attrs.sum
                    //console.log("hello world, I am working");
                    //console.log(view.name);
                    model.call("read", [event.id,[field]], {context: new instance.web.CompoundContext()}).then(function(result) 
                      {
                        //console.log("READ");
                        console.log(view);
                        var current_title = self.$el.find('.fc-header-title')[0].innerHTML
                        var end_title = current_title
                        if (current_title.search('Summary by field') >=0){
                            var newresult =0
                            if (self.fields_view.arch.attrs['view_title']!=view.title)
                                newresult = parseInt(result[field], 10)
                            else{
                                var str = current_title.split(': ')[1]
                                str = str.substring(0, str.length - 7)
                                newresult = parseInt(str, 10) + parseInt(result[field], 10);
                            }


                            end_title =  '<h2>'+view.title+'</h2><span>Summary by field '+self.fields_view.arch.attrs.sum+": "+newresult+'</span>' 
                        }
                        else{
                            
                            end_title = current_title +'<span>Summary by field '+self.fields_view.arch.attrs.sum+": "+result[field]+'</span>'    
                        }
                        self.fields_view.arch.attrs['view_title'] = view.title
                        //console.log(self.fields_view.arch.attrs['view_mode']);
                        self.$el.find('.fc-header-title').html(end_title);
                      });
                    var data = self.get_event_data(event);
                    //console.log(self.fields_view.arch.attrs)
                },
                eventAfterRender: function (event, element, view) {
                    if ((view.name !== 'month') && (((event.end-event.start)/60000)<=30)) {
                        //if duration is too small, we see the html code of img
                        var current_title = $(element.find('.fc-event-time')).text();
                        var new_title = current_title.substr(0,current_title.indexOf("<img")>0?current_title.indexOf("<img"):current_title.length);
                        element.find('.fc-event-time').html(new_title);
                    }
                },
                eventClick: function (event) { self.open_event(event._id,event.title); },
                select: function (start_date, end_date, all_day, _js_event, _view) {
                    var data_template = self.get_event_data({
                        start: start_date,
                        end: end_date,
                        allDay: all_day,
                    });
                    self.open_quick_create(data_template);

                },

                unselectAuto: false,


            });
        },


         });

};