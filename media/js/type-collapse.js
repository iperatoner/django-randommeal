window.addEvent('domready', function(){
	$$('.all-meals-list').set('slide', {duration: 350, mode: 'horizontal'});
	$$('.all-meals-list').set('fade', {duration: 250});
	$$('.all-meals-list').slide('hide');
	$$('.all-meals-list').fade('hide');
	
	$$('h3.meal-type-heading').addEvent('click', function(e){
		this.getNext().getElement('.all-meals-list').fade('toggle');
		this.getNext().getElement('.all-meals-list').slide('toggle');
	});
});