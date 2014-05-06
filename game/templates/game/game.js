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

    var loader = $.map(data.assets, function(value, key) {return value;})

            Q.Sprite.extend("Goal", {
                init: function(p) {
                    this._super(p, {asset: data.assets.goal});
                },
            });

            Q.Sprite.extend("Player", {
                init: function(p) {
                    this._super(p, {asset: data.assets.start, gravity:1.25});
                    this.add("2d, platformerControls");

                    this.on("hit.sprite", function(collision) {
                        if(collision.obj.isA("Goal"))
                        {
                            this.destroy();
                            endGame("You Won!");
                        }
                    });
                },

                step: function(dt) {
                    if (this.p.y > Q.height + data.spsize)
                    {
                        this.destroy();
                        endGame("You Died...");
                    }
                }
            });

            Q.Sprite.extend("Block", {
                init: function(p) {
                    this._super(p, {asset: data.assets.block});
                },
            });

            Q.Sprite.extend("Enemy", {
                init: function(p) {
                    this._super(p, {asset: data.assets.enemy, vx: 50,});
                    this.add("2d, aiBounce");

                    this.on("hit.sprite", function(collision) {
                        if(collision.obj.isA("Player")) {
                            collision.obj.destroy();
                            endGame("You Died...");
                        }
                    });
                },
            });

    Q.load(loader, function() {
        Q.scene("level", function(stage) {
            $.each(data.blocks, function(index, value) {
                stage.insert(new Q.Block({
                    x: (value.x * data.spsize + data.spsize/2),
                    y: (value.y * data.spsize + data.spsize/2)
                }));
            });

            $.each(data.enemies, function(index, value) {
                stage.insert(new Q.Enemy({
                    x: (value.x * data.spsize + data.spsize/2),
                    y: (value.y * data.spsize + data.spsize/2)
                }));
            });

            player = new Q.Player({
                x:data.start.x*data.spsize + data.spsize/2, 
                y:data.start.y*data.spsize + data.spsize/2
            });
            stage.insert(player);

            $.each(data.end, function(index, value) {
                goal = new Q.Goal({
                    x:value.x*data.spsize + data.spsize/2, 
                    y:value.y*data.spsize + data.spsize/2
                });
                stage.insert(goal);
            });
        });

        Q.stageScene("level");
        $('#quintus').focus();
    });

function endGame(message) {
    $('#gameOver').show();
    $('#gameOverMessage').html(message);
}

function restartStage() {
    Q.clearStages();
    Q.stageScene("level");
    $('#gameOver').hide();
    $('#quintus').focus();
}

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