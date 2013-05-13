jQuery(document).ready(function() {
    jQuery('body').midgardCreate({
	url: function () {
	    return this.getSubjectUri();
	},
	editorOptions: {
	    hallo: {
		plugins: {
		    'hallolink': {},
		    'halloimage': {},
		}
	    }
	}
    });
});

(function () {
    var csrftoken = $.cookie('csrftoken');
    var _sync = Backbone.sync;
    Backbone.sync = function(method, model, opts) {
	opts.beforeSend = function(request) {
	    $.noConflict();
	    request.setRequestHeader("X-CSRFToken", csrftoken);
	};
	return _sync(method, model, opts);
    }
})();
