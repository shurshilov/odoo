How to use
============

**Python

``@api.multi
    def somefunction(self):
    	#do something
        return {
                    'type': 'ir.actions.client',
                    'tag': 'popup_beauty.new',
                    'context':{
                                'body': result,
                                'button': 'OK',
                                'type': 'success',
                            },
                }``

**Javascript

``var action = {
                      'type': 'ir.actions.client',
                      'tag': 'popup_beauty.new',
                      'context':{
                                    'body': result,
                                    'button': 'OK',
                                    'type': 'success',
                                },
                };
    this.do_action(action)``

Contributors
------------

* Shurshilov Artem <shurshilov.a@yandex.ru>