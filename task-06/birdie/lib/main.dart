
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame/sprite.dart';
import 'package:flutter/material.dart';
import 'package:flame/flame.dart';
import 'package:flame_tiled/flame_tiled.dart';
import 'package:flutter/services.dart';


int horizontal = 0;
int vertical = 0;

void main() {
  runApp(GameWidget(game: Game()));
}

class Game extends FlameGame with TapCallbacks, KeyboardEvents {
  static late TiledComponent gameMap;
  static const int tileSize = 32;
  static const gravity = 0.5;
  static late Player player;

  @override
  Future<void> onLoad() async {
    gameMap = await TiledComponent.load('Cave.tmx', Vector2.all(tileSize.toDouble()));
    world.add(gameMap);

    double padding = 20.0;
    add(ControlButton(Vector2(ControlButton.controllerSize, size.y-ControlButton.controllerSize), "left"));
    add(ControlButton(Vector2(ControlButton.controllerSize*2+padding, size.y-ControlButton.controllerSize), "right"));
    add(ControlButton(Vector2(size.x-ControlButton.controllerSize, size.y-ControlButton.controllerSize*2-padding), "up"));
    add(ControlButton(Vector2(size.x-ControlButton.controllerSize, size.y-ControlButton.controllerSize), "down"));

    SpriteComponent backdrop = SpriteComponent();
    backdrop.sprite = await Sprite.load("../background.png");
    backdrop.size *= 3;
    player = Player(Vector2(250.0, 200.0));
    world.add(player);
    camera.viewfinder.position = Vector2(350.0, 200.0);
    camera.follow(player, maxSpeed: 300.0);
    camera.viewfinder.zoom = 3.0;
    camera.priority = -1;
    camera.backdrop.add(backdrop);
  }

  static bool tileAt(double x, double y) {
    return gameMap.tileMap.getTileData(layerId: 0, x: x~/tileSize, y: y~/tileSize)?.tile != 0;
  }

  @override
  KeyEventResult onKeyEvent(KeyEvent event, Set<LogicalKeyboardKey> keysPressed) {
    if (event is KeyDownEvent) {
      if (event.logicalKey == LogicalKeyboardKey.keyA) horizontal = -1;
      if (event.logicalKey == LogicalKeyboardKey.keyD) horizontal = 1;
      if (event.logicalKey == LogicalKeyboardKey.keyW) vertical = 1;
      if (event.logicalKey == LogicalKeyboardKey.keyS) vertical = -1;
    } else if (event is KeyUpEvent) {
      if (event.logicalKey == LogicalKeyboardKey.keyA || event.logicalKey == LogicalKeyboardKey.keyD) horizontal = 0;
      if (event.logicalKey == LogicalKeyboardKey.keyW || event.logicalKey == LogicalKeyboardKey.keyS) vertical = 0;
    }

    return KeyEventResult.handled;
  }
}

class HitBox {
  late Vector2 position;
  late Vector2 size;

  HitBox(this.size);

  void update(Vector2 pos) {
    position = pos;
  }

  bool touchingBottom() {
    int x = -1;
    for (int i = 0; i < size.x; i += Game.tileSize~/2) {
      if (i ~/ Game.tileSize != x) {
        x = i ~/ Game.tileSize;
        if (Game.tileAt(x + position.x, size.y/2 + position.y)) {
          return true;
        }
      }
    }
    return false;
  }

  bool touchingTop() {
    int x = -1;
    for (int i = 0; i < size.x; i += Game.tileSize~/2) {
      if (i ~/ Game.tileSize != x) {
        x = i ~/ Game.tileSize;
        if (Game.tileAt(x + position.x, position.y - size.y/2)) {
          return true;
        }
      }
    }
    return false;
  }

  bool touchingLeft() {
    int y = -1;
    for (int i=0; i<size.y; i+=Game.tileSize~/2)
    {
      if(i~/Game.tileSize != y)
      {
        y = i~/Game.tileSize;
        if (Game.tileAt(position.x-size.x/2, y+position.y))
        {
          return true;
        }
      }
    }
    return false;
  }

  bool touchingRight() {
    int y = -1;
    for (int i=0; i<size.y; i+=Game.tileSize~/2)
    {
      if(i~/Game.tileSize != y)
      {
        y = i~/Game.tileSize;
        if (Game.tileAt(position.x+size.x/2, y+position.y))
        {
          return true;
        }
      }
    }
    return false;
  }
}

class Player extends SpriteAnimationComponent with HasGameRef {
  late SpriteAnimation runAnimation;
  late SpriteAnimation attackAnimation;
  late SpriteAnimation jumpAnimation;
  late SpriteAnimation idleAnimation;
  Vector2 velocity = Vector2.zero();
  late HitBox hitBox;
  late bool touchingFloor = false;
  static const double speed = 50.0;
  static const double acceleration = 0.8;

  Player(Vector2 position) : super(position: position, anchor: Anchor.center, size: Vector2.all(64.0));

  @override
  Future<void> onLoad() async {
    var img = await Flame.images.load('../run.png');
    final runSpriteSheet = SpriteSheet(image: img, srcSize: Vector2.all(32));
    runAnimation = SpriteAnimation.fromFrameData(
      img,
      SpriteAnimationData([
        runSpriteSheet.createFrameDataFromId(0, stepTime: 0.1),
        runSpriteSheet.createFrameDataFromId(1, stepTime: 0.1),
        runSpriteSheet.createFrameDataFromId(2, stepTime: 0.1),
        runSpriteSheet.createFrameDataFromId(3, stepTime: 0.1),
      ]),
    );

    img = await Flame.images.load('../attack.png');
    final attackSpriteSheet = SpriteSheet(image: img, srcSize: Vector2.all(32));
    attackAnimation = SpriteAnimation.fromFrameData(
      img,
      SpriteAnimationData([
        attackSpriteSheet.createFrameDataFromId(0, stepTime: 0.1),
        attackSpriteSheet.createFrameDataFromId(1, stepTime: 0.1),
        attackSpriteSheet.createFrameDataFromId(2, stepTime: 0.1),
        attackSpriteSheet.createFrameDataFromId(3, stepTime: 0.1),
        attackSpriteSheet.createFrameDataFromId(4, stepTime: 0.1)
      ]),
    );

    img = await Flame.images.load('../jump.png');
    final jumpSpriteSheet = SpriteSheet(image: img, srcSize: Vector2.all(32));
    jumpAnimation = SpriteAnimation.fromFrameData(
      img,
      SpriteAnimationData([jumpSpriteSheet.createFrameDataFromId(0, stepTime: 0.1)]),
    );

    img = await Flame.images.load('../idle.png');
    final idleSpriteSheet = SpriteSheet(image: img, srcSize: Vector2.all(32));
    idleAnimation = SpriteAnimation.fromFrameData(
      img,
      SpriteAnimationData([
        idleSpriteSheet.createFrameDataFromId(0, stepTime: 0.1),
        idleSpriteSheet.createFrameDataFromId(1, stepTime: 0.1),
        idleSpriteSheet.createFrameDataFromId(2, stepTime: 0.1),
        idleSpriteSheet.createFrameDataFromId(3, stepTime: 0.1)
      ]),
    );

    animation = idleAnimation;

    hitBox = HitBox(Vector2(32.0, 32.0));
  }

  @override
  void update(double dt) {
    super.update(dt);
    velocity.y += Game.gravity;
    position += velocity;
    hitBox.update(position);
    bool last = touchingFloor;
    touchingFloor = false;

    if(velocity.y > 0) {
      while (hitBox.touchingBottom()) {
        position.y -= 1;
        velocity.y = 0.0;
        hitBox.update(position);
        touchingFloor = true;
      }
    } else {
      while (hitBox.touchingTop()) {
        position.y += 1;
        velocity.y = 0.0;
        hitBox.update(position);
      }
    }

    if(touchingFloor && vertical == 1) velocity.y = -10.0;

    velocity.x += (horizontal*speed-velocity.x)*acceleration*dt;

    velocity.x *= 0.9;

    if (velocity.x > 0) {
      while (hitBox.touchingRight()) {
        position.x -= 1;
        hitBox.update(position);
        velocity.x = 0.0;
      }
    } else {
      while (hitBox.touchingLeft()) {
        position.x += 1;
        hitBox.update(position);
        velocity.x = 0.0;
      }
    }

    if (velocity.x.abs() > 0.1) {
      animation = runAnimation;
      if (velocity.x > 0 && isFlippedHorizontally) flipHorizontally();
      if (velocity.x < 0 && !isFlippedHorizontally) flipHorizontally();
    } else {
      animation = idleAnimation;
    }
    if(!touchingFloor && !last) animation = jumpAnimation;
  }
}

class ControlButton extends SpriteComponent with TapCallbacks {
  static const controllerSize = 80.0;
  String type = "";

  ControlButton(Vector2 position, this.type)
    : super(
      position: position,
      anchor: Anchor.center,
      size: Vector2(controllerSize, controllerSize),
    ){
    priority = 100;
  }

  @override
  Future<void> onLoad() async {
    super.onLoad();
    sprite = await Sprite.load('../arrow-$type.png');
  }

  @override
  void onTapCancel(TapCancelEvent event) {
    if(type == "left" || type == "right") horizontal = 0;
    if(type == "down" || type == "up") vertical = 0;

    event.handled = true;
  }

  @override
  void onTapDown(TapDownEvent event) {
    if(type == "left") horizontal = -1;
    if(type == "right") horizontal = 1;
    if(type == "down") vertical = -1;
    if(type == "up") vertical = 1;

    event.handled = true;
  }

  @override
  void onTapUp(TapUpEvent event) {
    if(type == "left" || type == "right") horizontal = 0;
    if(type == "down" || type == "up") vertical = 0;

    event.handled = true;
  }
}