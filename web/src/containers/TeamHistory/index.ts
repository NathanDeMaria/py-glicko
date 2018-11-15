import { connect } from 'react-redux';

import { getTeamHistory } from 'src/actions/actionCreators';
import { IAppState } from 'src/interfaces';
import TeamHistory, { IOwnProps, IStateProps } from './TeamHistory';

const mapStateToProps = (state: IAppState, ownProps: IOwnProps): IStateProps => {
  const { league, team } = ownProps;
  const {
    teamHistory: {
      [league]: {
        [team]: history
      } = {}
    }
  } = state;
  return {history};
};

const mapDispatchToProps = (dispatch: any, ownProps: IOwnProps) => ({
  getTeamHistory: () => dispatch(getTeamHistory(ownProps.league, ownProps.team)),
});

export default connect(mapStateToProps, mapDispatchToProps)(TeamHistory as any); // TODO: typescript better
