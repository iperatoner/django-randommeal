window.addEvent('domready', function(){
	$$('.result-list > li .result-description').set('slide', {duration: 250});
	$$('.result-list > li').set('morph', {duration: 250});
	$$('.result-list > li .result-description').slide('hide');
	
	$$('.result-list > li').addEvent('click', function(e){
		if (!e.target.hasClass('button')) {
			if (this.hasClass('active')) {
				this.removeClass('active');
				this.morph(listitem_styles_inactive);
			}
			else {
				this.addClass('active');
				this.morph(listitem_styles_active);
			}
			this.getElement('.result-description').slide('toggle');
		}
	});
});