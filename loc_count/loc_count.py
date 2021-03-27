#!/usr/bin/env python3

import os
import re
import subprocess
import sys

LOC_SCRIPTS = {
    'locDeploymentSpecs': 'cloc_scripts/loc_deployment_specs.sh',
    'locGenModelsCustomerCore': 'cloc_scripts/loc_genmodels_customer_core.sh',
    'locGenModelsCustomerManagement':
        'cloc_scripts/loc_genmodels_customer_management.sh',
    'locManModelsLm': 'cloc_scripts/loc_manmodels_lm.sh'
}

LOC_BY_LANGS_SCRIPTS = {
    'locOpenApiCustomerCore': 'cloc_scripts/loc_openapi_customer_core.sh',
    'locOpenApiCustomerManagement':
        'cloc_scripts/loc_openapi_customer_management.sh'
}

VAR_NAME_PREFIX = 'zval'

def pipe_commands(commands=[], cwd=None):
    if not commands:
        return None

    outputs = []
    index = 0
    for cmd in commands:
        if not index:
            outputs.append(subprocess.Popen(cmd, cwd=cwd,
                stdout=subprocess.PIPE))
            index += 1
            continue

        previousOutput = outputs[index - 1]
        outputs.append(subprocess.Popen(cmd, stdin=previousOutput.stdout,
            stdout=subprocess.PIPE))
        index += 1

    output, error = outputs[-1].communicate()
    if error:
        raise RuntimeError('Error when executing "%s": %s' %
            (' '.join(outputs), error))
    return output.decode('utf-8').strip()

def get_absolute_path_and_file(filepath):
    abspath = os.path.abspath(filepath)
    folder = os.path.dirname(abspath)
    filename = os.path.basename(abspath)
    return folder, filename

def get_loc_sum(scriptFilepath, valueColumn=4):
    scriptFolder, scriptFilename = get_absolute_path_and_file(scriptFilepath)

    return pipe_commands([
        ['sh', scriptFilename],
        ['grep', 'SUM:'],
        ['awk', '{ print $%d }' % valueColumn],
    ], scriptFolder)

def get_loc_sums_by_languages(scriptFilepath, valueColumn=4):
    scriptFolder, scriptFilename = get_absolute_path_and_file(scriptFilepath)

    clocResult = pipe_commands([
        ['sh', scriptFilename],
        ['egrep', '(SUM:|[[:alpha:]]+)[[:blank:]]+[[:digit:]]+[[:blank:]]+' \
            '[[:digit:]]+[[:blank:]]+[[:digit:]]+[[:blank:]]+[[:digit:]]+']
    ], scriptFolder).split('\n')

    locByLangs = [l.split() for l in clocResult]
    locSumsByLanguages = {l[0]:l[valueColumn] for l in locByLangs}
    return locSumsByLanguages

def get_manual_adaptations(scriptFilepath):
    scriptFolder, scriptFilename = get_absolute_path_and_file(scriptFilepath)

    adaptationOutput = pipe_commands([
        ['sh', scriptFilename],
        ['grep', 'SUM'],
        ['head', '-n1'],
    ], scriptFolder)

    match = ADAPTATION_COUNT_PATTERN.match(adaptationOutput)
    return match.group('adaptationCount'), match.group('mandatoryCount')

def firstUpper(s):
    if s is None:
        return None
    elif len(s) == 0:
        return ''
    elif len(s) == 1:
        return s.upper()

    firstChar = s[0]
    remainingChars = s[1:]
    return firstChar.upper() + remainingChars

if __name__ == '__main__':
    texVars = {}

    for id, scriptDescription in LOC_SCRIPTS.items():
        if isinstance(scriptDescription, tuple):
            texVars[id] = get_loc_sum(scriptDescription[0],
                scriptDescription[1])
        else:
            texVars[id] = get_loc_sum(scriptDescription)

    for id, scriptDescription in LOC_BY_LANGS_SCRIPTS.items():
        locByLangs = get_loc_sums_by_languages(scriptDescription)
        for langName, loc in locByLangs.items():
            if langName != 'SUM:':
                texVars[id + langName] = loc
            else:
                texVars[id + 'LocByLangSum'] = loc

    varsText = '\n'.join(['\def \%s%s{%s}' %
        (VAR_NAME_PREFIX, firstUpper(k), v) for k, v in texVars.items()
    ])
    varsFile = open('tex_vars.tex', 'w')
    varsFile.write(varsText)
    varsFile.close()
