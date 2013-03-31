var Aloha = window.Aloha || ( window.Aloha = {} );
Aloha.settings = {
    locale: 'en',
    sidebar: {
	disabled: true
    },
    repositories: {
	linklist: {
	    data: [
		{ name: 'CreateJS Website', url:'http://createjs.org', type:'website' },
		{ name: 'CreateJS on Github', url:'https://github.com/bergie/create', type:'website' },
		{ name: 'Aloha Developers Wiki', url:'https://github.com/alohaeditor/Aloha-Editor/wiki', type:'website' },
		{ name: 'Aloha Editor - The HTML5 Editor', url:'http://aloha-editor.org', type:'website' },
		{ name: 'Aloha Editor Demos', url:'http://aloha-editor.org/demos.php', type:'website' },
		{ name: 'Aloha Editor Logo', url:'http://aloha-editor.org/logo/Aloha%20Editor%20HTML5%20contenteditable%20transparent%20512.png', type:'image' }
	    ]
	}
    },
    plugins: {
	format: {
	    config: [  'b', 'i', 'p', 'sub', 'sup', 'del', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'removeFormat' ]
	}
    }
}
