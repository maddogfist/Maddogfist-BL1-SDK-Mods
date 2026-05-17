import unrealsdk #type: ignore
from unrealsdk.hooks import Type, add_hook, remove_hook, Block, log_all_calls #type: ignore
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction #type: ignore
from mods_base import hook, get_pc, ENGINE, EInputEvent, keybind, build_mod, BoolOption #type: ignore

bool_lunge = True

allow_air_lunge = BoolOption("Allow Air Lunge",True)

@keybind(identifier="Disable Lunge", key="LeftShift", event_filter=None)
def PressLunge(event: EInputEvent):
    global bool_lunge
    if event is EInputEvent.IE_Pressed:
        bool_lunge = False
    elif event is EInputEvent.IE_Released:
        bool_lunge = True
    return

@hook("WillowGame.WillowPlayerController:CanLunge", Type.PRE)
def CanLunge(obj: UObject, args: WrappedStruct, ret: any, func: BoundFunction) -> bool:
    global bool_lunge
    
    if allow_air_lunge.value:
        if bool_lunge:
            return (True, True)
        return Block
    else:
        if int(get_pc().Pawn.OnGround) == 1:
            if bool_lunge:
                return (True, True)
            return Block
        return Block
        
build_mod(hooks=[CanLunge], keybinds=[PressLunge], options=[allow_air_lunge])