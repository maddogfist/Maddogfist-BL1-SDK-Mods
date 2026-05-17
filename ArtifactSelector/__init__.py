import unrealsdk #type: ignore
from unrealsdk import find_all #type: ignore
from unrealsdk.hooks import Type, add_hook, remove_hook, Block #type: ignore
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction, UScriptStruct#type: ignore
from mods_base import hook, get_pc, ENGINE, EInputEvent, keybind, build_mod #type: ignore

currentArtifactIndex = 0
                    
def getSkillHelper():
    skillhelper = find_all("SkillTreeGFxHelper")
    if skillhelper is None or len(skillhelper) < 2:
        return None
    return skillhelper[1]

def equipArtifact(ArtifactSkillIndex):
    if get_pc is None:
        return
    if ArtifactSkillIndex == -1:
        get_pc().ServerUnequipElementalSkill(get_pc().EquippedElementalSkillPlayerSkillIndex)
        return
    get_pc().ServerEquipElementalSkill(ArtifactSkillIndex)
    return
    
def formatMessage(ArtifactName):
    if "Explosive" in ArtifactName:
        return "<font color=\"#FDFF54\">" + ArtifactName + "</font>"
    elif "Incendiary" in ArtifactName:
        return "<font color=\"#FF3E29\">" + ArtifactName + "</font>"
    elif "Fire" in ArtifactName:
        return "<font color=\"#FF3E29\">" + ArtifactName + "</font>"
    elif "Shock" in ArtifactName:
        return "<font color=\"#385CFF\">" + ArtifactName + "</font>"
    elif "Corrosive" in ArtifactName:
        return "<font color=\"#23F741\">" + ArtifactName + "</font>"
    elif "Acid" in ArtifactName:
        return "<font color=\"#23F741\">" + ArtifactName + "</font>"
    else:
        return ArtifactName

@keybind(identifier="Next Artifact", key="Z", event_filter=EInputEvent.IE_Pressed)
def NextArtifact():
    global currentArtifactIndex
    
    if get_pc() is None:
        return
    
    helper = getSkillHelper()
    if helper is None:
        print("No SkillHelper found")
        get_pc().myHUD.GetHUDMovie().AddCriticalText(0, "Open up Skill Menu to activate Selector", 3.0, get_pc().myHUD.WhiteColor, get_pc().myHUD.WPRI)
        return

    artifacts = helper.ArtifactList
    if artifacts is None or len(artifacts) == 0:
        print("No Artifacts")
        return
        
    currentArtifactIndex += 1
    if currentArtifactIndex >= len(artifacts):
        currentArtifactIndex = 0
        
    equipArtifact(artifacts[currentArtifactIndex].SkillIndex)
    
    message = formatMessage(artifacts[currentArtifactIndex].Name)

    get_pc().myHUD.GetHUDMovie().AddCriticalText(0, message, 3.0, get_pc().myHUD.WhiteColor, get_pc().myHUD.WPRI)
    return
    
@keybind(identifier="Previous Artifact", event_filter=EInputEvent.IE_Pressed)
def PrevArtifact():
    global currentArtifactIndex
    
    if get_pc() is None:
        return
    
    helper = getSkillHelper()
    if helper is None:
        print("No SkillHelper found")
        get_pc().myHUD.GetHUDMovie().AddCriticalText(0, "Open up Skill Menu to activate Selector", 3.0, get_pc().myHUD.WhiteColor, get_pc().myHUD.WPRI)
        return

    artifacts = helper.ArtifactList
    if artifacts is None or len(artifacts) == 0:
        print("No Artifacts")
        return
        
    currentArtifactIndex -= 1
    if currentArtifactIndex < 0:
        currentArtifactIndex = len(artifacts)-1
        
    equipArtifact(artifacts[currentArtifactIndex].SkillIndex)
    
    message = formatMessage(artifacts[currentArtifactIndex].Name)

    get_pc().myHUD.GetHUDMovie().AddCriticalText(0, message, 3.0, get_pc().myHUD.WhiteColor, get_pc().myHUD.WPRI)
    return
    
build_mod(keybinds=[NextArtifact, PrevArtifact])