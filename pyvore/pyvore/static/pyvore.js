this.Pyvore = {
        cache: {},

        View: Backbone.View.extend({
            initialize: function() {
                if (this.model != undefined) {
                    this.model.on("change", function() {
                        this.render();
                    }, this);
                }

                if (this.collection != undefined) {
                    this.collection.on("reset", function() {
                        this.render();
                    }, this);
                }
            },

            serialize: function() {
                var context = {};

                var me = this;
                if (this.model != undefined) {
                    context['model'] = this.model.toJSON();
                }

                if (this.collection != undefined) {
                    context['collection'] = this.collection.toJSON();
                }

                return context;
            },

            save_model: function(e) {
                e.preventDefault();

                if (this.model != undefined) {
                    var me = this;

                    var data = me.$("form").serializeArray();
                    Pyvore.map_form_to_model(data, me.model);
                    console.log(me.model);
                    me.model.save({
                        error: function(e) {
                            console.log(e);
                        }
                    })
                }
            }
        }),

        Layout: Backbone.View.extend({
        }),

        ChangeView: Backbone.View.extend({
        }),

        map_form_to_model: function(data, model) {
            model.off("change");

            for(var i=0; i < data.length; i++) {
                var name = data[i].name;
                var value = data[i].value;

                var current_value = model.get(name);

                if (value != current_value) {
                    model.set(name, value);
                }
            }
        },

        // Assist with code organization, by breaking up logical components of code
        // into modules.
        module: function() {
            // Internal module cache.
            var modules = {};

            // Create a new module reference scaffold or load an existing module.
            return function(name) {
                // If this module has already been created, return it.
                if (modules[name]) {
                    return modules[name];
                }

                // Create a module and save it under this name
                return modules[name] = { 
                    Models: {},
                    Collections: {},
                    Views: {} 
                };
            };
        }(),

        // This is useful when developing if you don't want to use a
        // build process every time you change a template.
        //
        // Delete if you are using a different template loading method.
        fetchTemplate: function(path, done) {
            window.JST = window.JST || {};

            // Should be an instant synchronous way of getting the template, if it
            // exists in the JST object.
            if (JST[path]) {
                return done(JST[path]);
            }

            // Fetch it asynchronously if not available from JST
            return $.get("/static/app/templates/" + path +".html", function(contents) {
                var tmpl = Handlebars.compile(contents);
                JST[path] = tmpl;

                done(tmpl);
            });
        },

        // Keep active application instances namespaced under an app object.
        app: _.extend({}, Backbone.Events)
};
