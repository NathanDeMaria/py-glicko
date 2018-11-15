import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { getWeeklyUpdate } from 'src/actions/actionCreators';
import { IAppState } from 'src/interfaces';

import { IOwnProps, IStateProps, WeeklyUpdate } from './WeeklyUpdate';

const mapStateToProps = (state: IAppState, ownProps: IOwnProps): IStateProps => {
  const {weeklyUpdate: {[ownProps.season]: season}} = state;
  // Gotta be a better way to do this w/ null coalesing? Tuple key?
  if(!season) {
    return {
      weekResults: [],
    };
  }
  const {[ownProps.round]: weekResults} = season;
  return {
    weekResults,
  }
};
   
const mapDispatchToProps = (dispatch: any, ownProps: IOwnProps) => bindActionCreators({
  getWeeklyUpdate,
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(WeeklyUpdate as any); // TODO: typescript better
