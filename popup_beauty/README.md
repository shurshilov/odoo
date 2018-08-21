# How to use
### python
	@api.multi
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
                }
### javascript
    var action = {
                      'type': 'ir.actions.client',
                      'tag': 'popup_beauty.new',
                      'context':{
                                    'body': result,
                                    'button': 'OK',
                                    'type': 'success',
                                },
                };
    this.do_action(action)