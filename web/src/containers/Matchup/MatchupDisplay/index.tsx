import { connect } from 'react-redux';

import { IAppState } from 'src/interfaces';

import { default as MatchupDisplay, IStateProps} from './MatchupDisplay';

const mapStateToProps = (state: IAppState): IStateProps => {
    const { matchup: matchupState } = state;
    if(!matchupState) {
        return {
            team1: '',
            team2: '',
            matchup: null,
        }
    }
    const { team1, team2, matchup } = matchupState;
    return {
        team1,
        team2,
        matchup,
    }
};

export default connect(mapStateToProps)(MatchupDisplay as any); // TODO: typescript better
