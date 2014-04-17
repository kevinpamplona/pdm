{% if error %}
alert("{{error}}")
{% endif %}

{% autoescape off %}
data = jQuery.parseJSON('{{data}}');
{% endautoescape %}

{% load staticfiles %}

    var Q = Quintus()
                    .include("Sprites, Scenes, Input, 2D, UI, Touch")
                    .setup({width: data.width*data.spsize, height: data.height*data.spsize})
                    .controls().touch();

    var loader = []
    $.each(data.assets, function(key, value) {
        value = "{{STATIC_URL}}".concat(value);
        loader.push(value);
        
        if(key == data.end.ID)
        {
            Q.Sprite.extend("Goal", {
                init: function(p) {
                    this._super(p, {asset: value});
                },
            });
        }
        else if(key == data.start.ID)
        {
            Q.Sprite.extend("Player", {
                init: function(p) {
                    this._super(p, {asset: value, gravity:1.25});
                    this.add("2d, platformerControls");

                    this.on("hit.sprite", function(collision) {
                        if(collision.obj.isA("Goal"))
                        {
                            Q.stageScene("endGame", 1, {label: "You won!"});
                            this.destroy();
                        }
                    });
                },

                step: function(dt) {
                    if (this.p.y > Q.height + data.spsize)
                    {
                        Q.stageScene("endGame", 1, {label: "You died..."});
                        this.destroy();
                    }
                }
            });
        }
        else
        {
            Q.Sprite.extend("Block" + key.charCodeAt(0).toString(), {
                init: function(p) {
                    this._super(p, {asset: value})
                },
            });
        }
    });

    Q.load(loader, function() {
        Q.scene("level", function(stage) {
            $.each(data.blocks, function(index, value) {
                var evalstr = "stage.insert(".concat(
                    "new Q.Block", value.ID.charCodeAt(0).toString(), "(",
                        "{x:", (value.x * data.spsize + data.spsize/2).toString(),
                        ",y:", (value.y * data.spsize + data.spsize/2).toString(),
                        "}",
                    "));" );
                (new Function('stage', 'Q', evalstr))(stage, Q);
            });

            player = new Q.Player({
                x:data.start.x*data.spsize + data.spsize/2, 
                y:data.start.y*data.spsize + data.spsize/2
            });
            stage.insert(player);

            goal = new Q.Goal({
                x:data.end.x*data.spsize + data.spsize/2, 
                y:data.end.y*data.spsize + data.spsize/2
            });
            stage.insert(goal);
        });

        Q.scene('endGame',function(stage) {
            var box = stage.insert(new Q.UI.Container({
                x: Q.width/2, y: Q.height/2, fill: "rgba(0,0,0,0.5)"
            }));
  
            var button = box.insert(new Q.UI.Button({ x: 0, y: 0, fill: "#CCCCCC",
                                           label: "Play Again" }))         
            var label = box.insert(new Q.UI.Text({x:10, y: -10 - button.p.h, 
                                        label: stage.options.label }));
            button.on("click",function() {
                Q.clearStages();
                Q.stageScene("level");
            });
            box.fit(20);
        });

        Q.stageScene("level");
    });


/*
Q.Sprite.extend("Block", {
    init: function(p) {
        this._super(p, {asset: "Block.gif",});

        //this.add("2d");
    },
});

Q.Sprite.extend("Player", {
    init: function(p) {
        this._super(p, {asset: "Kirby.gif",});

        this.add("2d, platformerControls");
    },
});

Q.load(["Kirby.gif", "Block.gif",
        ], function() {
    Q.scene("testlevel", function(stage) {
        player = new Q.Player({x:Q.width/2,});
        block = new Q.Block({x:Q.width/2,y:Q.height/2});
        stage.insert(player);
        stage.insert(block);    
    });

    Q.stageScene("testlevel");

});
*/