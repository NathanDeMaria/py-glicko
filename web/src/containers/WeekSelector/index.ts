import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { getSeasons } from 'src/actions/actionCreators';
import { IAppState } from 'src/interfaces';

import { IOwnProps, IStateProps, WeekSelector } from './WeekSelector';

const mapStateToProps = (state: IAppState, ownProps: IOwnProps): IStateProps => {
  const {weekSelector: {[ownProps.league]: seasons}} = state;
  return {
    seasons,
  };
};
   
const mapDispatchToProps = (dispatch: any) => bindActionCreators({
  getSeasons,
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(WeekSelector as any); // TODO: typescript better
