import random

from alttprbot.alttprgen import preset, smz3multi

from .core import SahasrahBotCoreHandler


class GameHandler(SahasrahBotCoreHandler):
    async def ex_multiworld(self, args, message):
        if await self.is_locked(message):
            return

        try:
            preset_name = args[0]
        except IndexError:
            await self.send_message(
                'You must specify a preset!'
            )
            return

        if self.data.get('team_race', False) is False:
            await self.send_message('This must be a team race.')
            return

        if not self.is_equal_teams:
            await self.send_message("Teams are unequal in size.")
            return

        await self.send_message("Generating game, please wait.  If nothing happens after a minute, contact Synack.")

        seed_number = random.randint(0, 2147483647)

        try:
            teams = self.teams
            for team in teams:
                seed = await smz3multi.generate_multiworld(preset_name, teams[team], tournament=True, randomizer='smz3', seed_number=seed_number)
                await self.send_message(f"Team {team}: {seed.url}")
                await self.send_message("------")
        except Exception as e:
            await self.send_message(str(e))
            return

        race_info = f"SMZ3 Multiworld - {preset_name}"
        await self.set_raceinfo(race_info)
        await self.send_message("Seed rolling complete.")
        self.seed_rolled = True

    async def ex_preset(self, args, message):
        await self.roll_game(args, message)

    async def ex_race(self, args, message):
        await self.roll_game(args, message)

    async def ex_help(self, args, message):
        await self.send_message("Available commands:\n\"!race <preset>, !multiworld <preset>\" to generate a race preset.  Check out https://sahasrahbot.synack.live/rtgg.html#smz3-commands for more info.")

    async def roll_game(self, args, message):
        if await self.is_locked(message):
            return

        try:
            preset_name = args[0]
        except IndexError:
            await self.send_message(
                'You must specify a preset!'
            )
            return

        await self.send_message("Generating game, please wait.  If nothing happens after a minute, contact Synack.")
        try:
            seed, _ = await preset.get_preset(preset_name, randomizer='smz3', spoilers="off")
        except preset.PresetNotFoundException as e:
            await self.send_message(str(e))
            return

        race_info = f"{preset_name} - {seed.url} - ({seed.code})"
        await self.set_raceinfo(race_info)
        await self.send_message(seed.url)
        await self.send_message("Seed rolling complete.  See race info for details.")
        self.seed_rolled = True
