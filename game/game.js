var Q = Quintus()
                .include("Sprites, Scenes, Input, 2D, UI")
                .setup().controls();

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