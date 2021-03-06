window.addEvent('domready', function(){
	Element.implement({
		
		// Method to enable the fieldset belonging to this legend
		enableFieldset: function(){
			var fieldset = this.getParent().getParent();
			
			fieldset.morph(listitem_styles_active);
			fieldset.addClass(listitem_active_class);
			
			// Re-enable all items in this fieldset
			fieldset.getElements('> input[type=checkbox], select').each(function(el){
				el.setProperty('disabled', false);
				
				// Enabling the custom range box, if this is a select-element and 'custom' was selected
				if (el.get('tag') == 'select' && el.value == 'custom') {
					el.enableCustomRange();
				}
			});
		},

		// Method to disable the fieldset belonging to this legend
		disableFieldset: function(){
			var fieldset = this.getParent().getParent();
			
			fieldset.morph(listitem_styles_inactive);
			fieldset.removeClass(listitem_active_class);

			// Disable all items in this fieldset
			fieldset.getElements('> input[type=checkbox], select').each(function(el){
				el.setProperty('disabled', true);
				
				// Disabling the custom range box, if this is a select box
				if (el.get('tag') == 'select') {
					el.disableCustomRange();
				}
			});
		}
	});
	
	$$('fieldset').set('morph', {duration: 150});
	
	var filter_select_fn = function(el){
		/* The method `addEvent` uses the event as the first argument. */
		if (instanceOf(el, Event)) {
			el = this;
		}
		if (el.getProperty('checked')) {
			el.enableFieldset();
		}
		else {
			el.disableFieldset();
		}
	};
	
	$$('fieldset legend input[type=checkbox]').each(filter_select_fn);
	$$('fieldset legend input[type=checkbox]').addEvent('change', filter_select_fn);
});