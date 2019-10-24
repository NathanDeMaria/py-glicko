import { connect } from 'react-redux';

import { getMatchup, getTeams } from 'src/actions/actionCreators';
import { IAppState } from 'src/interfaces';

import { default as TeamSelector, IOwnProps, IStateProps} from './TeamSelector';

const mapStateToProps = (state: IAppState, ownProps: IOwnProps): IStateProps => {
  const { league } = ownProps;
  const { leagueTeams: { [league]: teams = [] } = {} } = state;
  return {
    teams,
  };
};
   
const mapDispatchToProps = (dispatch: any, ownProps: IOwnProps) => ({
  getMatchup: (team1: string, team2: string) => dispatch(getMatchup(ownProps.league, team1, team2)),
  getTeams: () => dispatch(getTeams(ownProps.league)),
});

export default connect(mapStateToProps, mapDispatchToProps)(TeamSelector as any); // TODO: typescript better
