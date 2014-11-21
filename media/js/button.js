;(function(d){var k=d.scrollTo=function(a,i,e){d(window).scrollTo(a,i,e)};k.defaults={axis:'xy',duration:parseFloat(d.fn.jquery)>=1.3?0:1};k.window=function(a){return d(window)._scrollable()};d.fn._scrollable=function(){return this.map(function(){var a=this,i=!a.nodeName||d.inArray(a.nodeName.toLowerCase(),['iframe','#document','html','body'])!=-1;if(!i)return a;var e=(a.contentWindow||a).document||a.ownerDocument||a;return d.browser.safari||e.compatMode=='BackCompat'?e.body:e.documentElement})};d.fn.scrollTo=function(n,j,b){if(typeof j=='object'){b=j;j=0}if(typeof b=='function')b={onAfter:b};if(n=='max')n=9e9;b=d.extend({},k.defaults,b);j=j||b.speed||b.duration;b.queue=b.queue&&b.axis.length>1;if(b.queue)j/=2;b.offset=p(b.offset);b.over=p(b.over);return this._scrollable().each(function(){var q=this,r=d(q),f=n,s,g={},u=r.is('html,body');switch(typeof f){case'number':case'string':if(/^([+-]=)?\d+(\.\d+)?(px|%)?$/.test(f)){f=p(f);break}f=d(f,this);case'object':if(f.is||f.style)s=(f=d(f)).offset()}d.each(b.axis.split(''),function(a,i){var e=i=='x'?'Left':'Top',h=e.toLowerCase(),c='scroll'+e,l=q[c],m=k.max(q,i);if(s){g[c]=s[h]+(u?0:l-r.offset()[h]);if(b.margin){g[c]-=parseInt(f.css('margin'+e))||0;g[c]-=parseInt(f.css('border'+e+'Width'))||0}g[c]+=b.offset[h]||0;if(b.over[h])g[c]+=f[i=='x'?'width':'height']()*b.over[h]}else{var o=f[h];g[c]=o.slice&&o.slice(-1)=='%'?parseFloat(o)/100*m:o}if(/^\d+$/.test(g[c]))g[c]=g[c]<=0?0:Math.min(g[c],m);if(!a&&b.queue){if(l!=g[c])t(b.onAfterFirst);delete g[c]}});t(b.onAfter);function t(a){r.animate(g,j,b.easing,a&&function(){a.call(this,n,b)})}}).end()};k.max=function(a,i){var e=i=='x'?'Width':'Height',h='scroll'+e;if(!d(a).is('html,body'))return a[h]-d(a)[e.toLowerCase()]();var c='client'+e,l=a.ownerDocument.documentElement,m=a.ownerDocument.body;return Math.max(l[h],m[h])-Math.min(l[c],m[c])};function p(a){return typeof a=='object'?a:{top:a,left:a}}})(jQuery);
jQuery.fn.topLink = function(settings) {
	settings = jQuery.extend({
		min: 1,
		fadeSpeed: 200
	}, settings);
	return this.each(function() {
	var el = $(this);
	el.hide();
	$(window).scroll(function() {
		//ie hack
		if(!jQuery.support.hrefNormalized) {
			el.css({
				'position': 'absolute',
				'bottom': $(window).scrollTop() + $(window).height() - settings.ieOffset
			});
		}
	ael = el.children('a');
	if($(window).scrollTop() >= settings.min) {
		el.fadeIn(settings.fadeSpeed);
		ael.html('<span id="topicon"></span>наверх').parent().removeClass('bottom_button').addClass('top_button');
	} else {
		ael.html('<span id="backicon"></span>вниз').parent().removeClass('top_button').addClass('bottom_button');
	}
	
	});
	});
};
$(document).ready(function(){
	$('#top-link').css({'': $(window).height()});
	function mytoplink() { // функция проверки
		var h = $(window).width()/2-1000/2-100;
		// 800 - ширина сайта (обычно #wrapper)
		// 100 - ширина собственно кнопки
		$('#top-link').removeClass('veryhidden');
		$('#top-link').css({'': h+'px'});		
	}
	mytoplink(); // вызываем функцию проверки при загрузке страницы
	$(window).resize(function(){
	// вызываем функцию проверки при изменении размеров окна браузера
		mytoplink();
	});
	$('#top-link').topLink({min: 400,fadeSpeed: 500});
	$('#top-link').click(function(e) {
		if($(this).hasClass('bottom_button')){
			jQuery("body").scrollTo( pos + 'px', 500 );
		} else{
			pos = (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;
			jQuery("body,html").animate({scrollTop: 0},500);
		}
		return false;
	});
});
