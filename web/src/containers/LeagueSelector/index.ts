import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { getLeagues } from 'src/actions/actionCreators';
import { IAppState } from 'src/interfaces';

import { IStateProps, LeagueSelector } from './LeagueSelector';

const mapStateToProps = (state: IAppState): IStateProps => {
  const {leagueSelector} = state;
  return {
    leagues: leagueSelector,
  };
};

const mapDispatchToProps = (dispatch: any) => bindActionCreators({
  getLeagues,
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(LeagueSelector as any); // TODO: typescript better
