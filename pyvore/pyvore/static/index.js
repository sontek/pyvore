// Treat the jQuery ready function as the entry point to the application.
// Inside this function, kick-off all initialization, everything up to this
// point should be definitions.
jQuery(function($) {
    Pyvore.socket = io.connect('/chat');

    Pyvore.socket.on("connect", function () {
        // we are connected... nothing to do really
    });

    Backbone.LayoutManager.configure({
        // pull templates from JST
        fetch: function(name) {
            return window.JST[name];
        },

        render: function(template, context) {
            return template(context);
        }
    });

    // Show a loader image on ajax requests
    $(document).ajaxStart(function(){ 
        $('.loader').show();
    }).ajaxStop(function(){ 
        $('.loader').hide();
    });


    // Shorthand the application namespace
    var app = Pyvore.app;

    // Include the example module
    var Sessions = Pyvore.module("sessions");

    // Defining the application router, you can attach sub routers here.
    var Router = Backbone.Router.extend({
        use_layout: function(name, container) {
            var me = this;
            var currentLayout = this.currentLayout;

            // If there is an existing layout and its the current one, return it.
            if (currentLayout && currentLayout.options.template == name) {
                return currentLayout;
            }

            // Create the new layout and set it as current.
            this.currentLayout = new Backbone.LayoutManager({
                template: name
            });

            this.currentLayout.render(function(el) {
                $(container).html(el);
            });

            return this.currentLayout;
        },

        routes: {
            "": "index",
            "chat/:id": "chat"
        },

        render_sessions: function() {
            if (user_name != undefined) {
                var me = this;
                var layout = this.use_layout("main_layout", "#container-body");


                if (Pyvore.sessions == undefined) {
                    Pyvore.sessions = new Sessions.Collections.SessionCollection();
                    Pyvore.sessions.fetch();
                }


                var session_list = new Sessions.Views.SessionList({
                    collection: Pyvore.sessions
                })

                layout.view('#session_list', session_list);

                session_list.render();

                return layout;
            }
        },

        index: function() {
            console.log("index");
            this.render_sessions();
        },

        chat: function(id) {
            Pyvore.socket.emit("subscribe", {'id': id})

            var me = this;
            var layout = this.render_sessions();

            var chatlog = new Sessions.Collections.Chat({}, id);

            var chat_view = new Sessions.Views.ChatList({
                collection: chatlog
            })

            chatlog.fetch();

            layout.view("#chat_window", chat_view);
            chat_view.render();
        }

    });

    // Define your master router on the application namespace and trigger all
    // navigation from this instance.
    app.router = new Router();

    // All navigation that is relative should be passed through the navigate
    // method, to be processed by the router.  If the link has a data-bypass
    // attribute, bypass the delegation completely.
    $(document).on("click", "a:not([data-bypass])", function(evt) {
        // Get the anchor href and protcol
        var href = $(this).attr("href");
        var protocol = this.protocol + "//";

        var cls = $(this).attr('class');
        if (cls != undefined) {
            if(cls.match(/\bui-/) || cls.match(/\bchzn/) || cls.match(/\bplupload/)) {
                return;
            }
        }

        // Ensure the protocol is not part of URL, meaning its relative.
        if (href && href.slice(0, protocol.length) !== protocol) {
            // Stop the default event to ensure the link will not cause a page
            // refresh.
            evt.preventDefault();

            // This uses the default router defined above, and not any routers
            // that may be placed in modules.  To have this work globally (at the
            // cost of losing all route events) you can change the following line
            // to: Backbone.history.navigate(href, true);
            app.router.navigate(href.substring(1), true);
        }
    });

    // Trigger the initial route and enable HTML5 History API support
    Backbone.history.start({ pushState: true });
});
