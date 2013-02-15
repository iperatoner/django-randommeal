window.addEvent('domready', function(){
	Element.implement({
		enableCustomRange: function() {
			var next = this.getNext('.deactivable-elements');
			next.removeClass('inactive');
			next.addClass('active');
			next.getElements('input').setProperty('disabled', false);
			next.fade('in');
		},
		disableCustomRange: function() {
			var next = this.getNext('.deactivable-elements');
			next.removeClass('active');
			next.addClass('inactive');
			next.getElements('input').setProperty('disabled', true);
			next.fade(0.1);
		}
	});
	
	var deactivable_elements = $$('.deactivable-elements');
	
	deactivable_elements.setStyle('opacity', 0.1);
	$$('.deactivable-elements input').setProperty('disabled', true);
	
	$$('fieldset select').addEvent('change', function(){
		if (this.value == 'custom') {
			this.enableCustomRange();
		}
		else {
			this.disableCustomRange();
		}
	});
});