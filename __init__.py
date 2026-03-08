''' Heat generator for ladders '''

import logging
import RHUtils
import random
from eventmanager import Evt
from HeatGenerator import HeatGenerator, HeatPlan, HeatPlanSlot, SeedMethod
from RHUI import UIField, UIFieldType, UIFieldSelectOption
from .heat_sizes import generate_heat_sizes

logger = logging.getLogger(__name__)

def getTotalPilots(rhapi, generate_args):
    input_class_id = generate_args.get('input_class')

    if input_class_id:
        if generate_args.get('total_pilots'):
            total_pilots = int(generate_args['total_pilots'])
        else:
            race_class = rhapi.db.raceclass_by_id(input_class_id)
            class_results = rhapi.db.raceclass_results(race_class)
            # Do I have a result of input class?
            if class_results and type(class_results) == dict:
                # fill from available results
                total_pilots = len(class_results['by_race_time'])
            else:
                # fall back to all pilots
                total_pilots = len(rhapi.db.pilots)
    else:
        # use total number of pilots
        total_pilots = len(rhapi.db.pilots)

    return total_pilots

def generateBalancedLadder(rhapi, generate_args=None):
    available_seats = generate_args.get('available_seats')
    suffix = rhapi.__(generate_args.get('suffix', 'Main'))

    total_pilots = getTotalPilots(rhapi, generate_args)

    if total_pilots == 0:
        logger.warning("Unable to seed ladder: no pilots available")
        return False

    letters = rhapi.__('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    heats = []

    if 'seed_offset' in generate_args:
        seed_offset = max(int(generate_args['seed_offset']) - 1, 0)
    else:
        seed_offset = 0

    # Reverse the list to ensure descending order
    unseeded_pilots = sorted(list(range(seed_offset, total_pilots + seed_offset)), reverse=True)

    # Calculate the number of heats needed and distribute pilots inversely
    heat_sizes = generate_heat_sizes(total_pilots)
    num_heats = (total_pilots + available_seats - 1) // available_seats  # Ceiling division
    pilots_per_heat = total_pilots // num_heats
    extra_pilots = total_pilots % num_heats

    for heat_index, heat_size in enumerate(heat_sizes):
        heat = HeatPlan(
            letters[heat_index] + ' ' + suffix,
            []
        )

        # Determine the number of pilots for this heat inversely
        for _ in range(heat_size):
            if unseeded_pilots:
                heat.slots.append(HeatPlanSlot(SeedMethod.INPUT, unseeded_pilots.pop(0) + 1))

        heats.append(heat)

    return heats

def register_handlers(args):
    for generator in [
        HeatGenerator(
            "La Lligueta: Ranked balanced fill",
            generateBalancedLadder,
            {
                'advances_per_heat': 0,
            },
            [
                UIField('total_pilots', "Maxiumum pilots in class", UIFieldType.BASIC_INT, placeholder="Auto", desc="Total pilots in next generated heat. Fallback to number of pilots of input class or all pilots in DB"),
                UIField('seed_offset', "Seed from rank", UIFieldType.BASIC_INT, value=1),
                UIField('suffix', "Heat title suffix", UIFieldType.TEXT, placeholder="Main", value="Main"),
            ],
        ),
    ]:
        args['register_fn'](generator)

def initialize(rhapi):
    rhapi.events.on(Evt.HEAT_GENERATOR_INITIALIZE, register_handlers)

