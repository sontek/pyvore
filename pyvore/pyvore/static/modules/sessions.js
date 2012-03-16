(function(Sessions) {
    Sessions.Views.SessionList = Pyvore.View.extend({
        template: "session_list"
    });

    Sessions.Models.Chat = Backbone.Model.extend({
    });

    Sessions.Views.ChatItem = Pyvore.View.extend({
        template: "chatitem"
    });

    Sessions.Views.ChatList = Pyvore.View.extend({
        events: {
            "click #send": "send",
            "keydown #txtChat": "check_send"
        },

        template: "chat",

        render: function(manage) {
            var me = this;
            var view = manage(this);
            if (this.collection != undefined) {
                this.collection.each(function(model) {
                    view.insert("ul", new Sessions.Views.ChatItem({
                        model: model
                    }));
                });
            }
            return view.render();
        },

        serialize: function() {
            var me = this;

            context = Pyvore.View.prototype.serialize.call(this);

            var session = '';

            for(var i=0; i < Pyvore.sessions.models.length; i++) {
                if (Pyvore.sessions.models[i].id == me.collection.pk) {
                    session = Pyvore.sessions.models[i];
                }
            }

            if (session != '') {
                context['session'] = session.toJSON();
            }

            return context;
        },

        initialize: function() {
            var me = this;

            Pyvore.View.prototype.initialize.call(this);

            this.collection.on("add", function(model) {
                var view = new Sessions.Views.ChatItem({
                    model: model
                })

                this.view("ul", view, true).render();
                me.$("ul").scrollTop(me.$("ul").get(0).scrollHeight);

            }, this);

            Pyvore.socket.on("chat", function (data) {
                console.log("DATA!!!", data);

                if (data.session_pk == me.collection.pk) {
                    me.collection.add(data)
                }

            });
        },

        check_send: function(event) {
            if (event.keyCode == 13) {
                this.send();
            }
        },

        send: function() {
            var val = this.$("#txtChat").val();
            var id = this.collection.pk;
            Pyvore.socket.emit("chat", this.collection.pk, val);
            this.$("#txtChat").val("");
        }
    });

    Sessions.Collections.Chat = Backbone.Collection.extend({
        initialize: function(models, pk) {
            var me = this;
            this.pk = pk;
        },

        url: function () {
            return '/api/sessions/' + this.pk
        }
    });

    Sessions.Collections.SessionCollection = Backbone.Collection.extend({
        url: '/api/sessions/'
    });

})(Pyvore.module("sessions"));
