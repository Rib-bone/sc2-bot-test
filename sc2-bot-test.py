import random
import sc2
from sc2 import Race, Difficulty, UnitTypeId
from sc2.constants import AbilityId
from sc2.ids.buff_id import BuffId
from sc2.units import Units
from sc2.player import Bot, Computer
class ThreebaseVoidrayBot(sc2.BotAI):
    def select_target(self, state):
        if self.enemy_structures.exists:
            return random.choice(self.enemy_structures)
        return self.enemy_start_locations[0]
    def get_random_pos(self):
        return [random.randrange(-5, 5), random.randrange(-5, 5)]
    async def defensive_patrol(self):
        location = random.choice(self.townhalls).position.to2 + self.get_random_pos()
        for unit in self.defencive_force.idle:
            self.do(unit.attack(location))
    async def on_step(self, iteration):
        if iteration == 0:
            self.defencive_force: Units = Units([], self)
            self.attack_force: Units = Units([], self)
            await self.chat_send("(glhf)")
        if not self.townhalls.ready:
            for worker in self.workers:
                self.do(worker.attack(self.enemy_start_locations[0]))
            return
        else:
            nexus = self.townhalls.ready.random
        if not nexus.has_buff(BuffId.CHRONOBOOSTENERGYCOST):
            abilities = await self.get_available_abilities(nexus)
            if AbilityId.EFFECT_CHRONOBOOSTENERGYCOST in abilities:
                self.do(nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus))
        for idle_worker in self.workers.idle:
            mf = self.mineral_field.closest_to(idle_worker)
            self.do(idle_worker.gather(mf))
        if iteration % 20 == 0:
            for vr in self.attack_force:
                self.do(vr.attack(self.select_target(self.state)))
        if self.defencive_force.amount >= 10 and self.attack_force.amount < 10:
            self.attack_force = self.defencive_force
            self.defencive_force = Units([], self)
        else:
            self.defencive_force += (self.units(UnitTypeId.VOIDRAY).idle - self.attack_force - self.defencive_force)
            await self.defensive_patrol()
        for a in self.structures(UnitTypeId.ASSIMILATOR):
            if a.assigned_harvesters < a.ideal_harvesters:
                w = self.workers.closer_than(20, a)
                if w.exists:
                    self.do(w.random.gather(a))
        if self.supply_left < 4 and not self.already_pending(UnitTypeId.PYLON):
            if self.can_afford(UnitTypeId.PYLON):
                await self.build(UnitTypeId.PYLON, near=nexus)
            return
        if self.workers.amount < self.townhalls.amount*15 and nexus.is_idle:
            if self.can_afford(UnitTypeId.PROBE):
                self.do(nexus.train(UnitTypeId.PROBE))
        elif not self.units(UnitTypeId.PYLON).exists and not self.already_pending(UnitTypeId.PYLON):
            if self.can_afford(UnitTypeId.PYLON):
                await self.build(UnitTypeId.PYLON, near=nexus)
        if self.townhalls.amount < 3 and not self.already_pending(UnitTypeId.NEXUS):
            if self.can_afford(UnitTypeId.NEXUS):
                await self.expand_now()
        if self.units(UnitTypeId.PYLON).ready.exists:
            pylon = self.units(UnitTypeId.PYLON).ready.random
            if self.units(UnitTypeId.GATEWAY).ready.exists:
                if not self.units(UnitTypeId.CYBERNETICSCORE).exists:
                    if self.can_afford(UnitTypeId.CYBERNETICSCORE) and not self.already_pending(UnitTypeId.CYBERNETICSCORE):
                        await self.build(UnitTypeId.CYBERNETICSCORE, near=pylon)
            else:
                if self.can_afford(UnitTypeId.GATEWAY) and not self.already_pending(UnitTypeId.GATEWAY):
                    await self.build(UnitTypeId.GATEWAY, near=pylon)
        for nexus in self.townhalls.ready:
            vgs = self.vespene_geyser.closer_than(20.0, nexus)
            for vg in vgs:
                if not self.can_afford(UnitTypeId.ASSIMILATOR):
                    break
                worker = self.select_build_worker(vg.position)
                if worker is None:
                    break
                if not self.gas_buildings or not self.gas_buildings.closer_than(1, vg):
                    self.do(worker.build(UnitTypeId.ASSIMILATOR, vg), subtract_cost=True)
                    self.do(worker.stop(queue=True))
        if self.structures(UnitTypeId.PYLON).ready.exists and self.structures(UnitTypeId.CYBERNETICSCORE).ready.exists:
            pylon = self.units(UnitTypeId.PYLON).ready.random
            if self.structures(UnitTypeId.STARGATE).amount < 3 and not self.already_pending(UnitTypeId.STARGATE):
                if self.can_afford(UnitTypeId.STARGATE):
                    await self.build(UnitTypeId.STARGATE, near=pylon)
        for stargate in self.structures(UnitTypeId.STARGATE).ready.idle:
            if self.can_afford(UnitTypeId.VOIDRAY):
                self.do(stargate.train(UnitTypeId.VOIDRAY))
def main():
    sc2.run_game(sc2.maps.get("(2)CatalystLE"), [
        Bot(Race.Protoss, ThreebaseVoidrayBot()),
        Computer(Race.Terran, Difficulty.Easy)
    ], realtime=False)
if __name__ == '__main__':
    main()
