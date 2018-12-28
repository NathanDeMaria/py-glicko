import { connect } from 'react-redux';

import { getTeamHistory, getTeams } from 'src/actions/actionCreators';
import { IAppState } from 'src/interfaces';
import TeamPicker, { IOwnProps, IStateProps } from './TeamPicker';

const mapStateToProps = (state: IAppState, ownProps: IOwnProps): IStateProps => {
  const { league } = ownProps;
  const { teamsPicker: { [league]: teams = [] } = {} } = state;
  return {
    teams,
  };
};

const mapDispatchToProps = (dispatch: any, ownProps: IOwnProps) => ({
  getTeamHistory: (team: string) => dispatch(getTeamHistory(ownProps.league, team)),
  getTeams: () => dispatch(getTeams(ownProps.league)),
});

export default connect(mapStateToProps, mapDispatchToProps)(TeamPicker as any); // TODO: typescript better
