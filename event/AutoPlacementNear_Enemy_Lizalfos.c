-------- EventFlow: AutoPlacementNear_Enemy_Lizalfos --------

Actor: AutoPlacement
entrypoint: None()
actions: ['CreateData', 'NearCreate']
queries: ['GroundNorm', 'WaterDepth', 'EcoAreaActorName', 'PlayerRideHorse', 'GroundMat', 'TimeType', 'CheckGameData', 'RouteDistance']
params: None

void EntryPoint0() {

    fork {
        if AutoPlacement.EcoAreaActorName({'ActorName': 'Enemy_Lizalfos_Electric'}) {
            if AutoPlacement.CheckGameData({'Label': 'FirstTouchdown'}) {
                if AutoPlacement.GroundMat() in [3, 12] {
                    Event267:
                    if AutoPlacement.TimeType() in [3, 5] {
                        if !AutoPlacement.PlayerRideHorse() {
                            AutoPlacement.NearCreate({'WaitFrame': 1})
                            if AutoPlacement.GroundNorm({'Angle': 10.0}) {
                                if !AutoPlacement.WaterDepth({'Depth': 0.0}) {
                                    if AutoPlacement.RouteDistance({'Distance': 20.0}) {
                                        AutoPlacement.CreateData({'MinNum': 1, 'OffsetPosY': 0.0, 'RideList': '', 'MaxNum': 1, 'GroupRadius': 1.0, 'EquipWeaponActorCount': -1, 'Mimicry': False})
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    } {
        if AutoPlacement.EcoAreaActorName({'ActorName': 'Enemy_Lizalfos_Ice'}) {
            if AutoPlacement.CheckGameData({'Label': 'FirstTouchdown'}) {
                if AutoPlacement.GroundMat() in [9, 14] {
                    goto Event267
                }
            }
        }
    }

}
