import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import { getWeeklyUpdate } from 'src/actions/actionCreators';
import WeeklyUpdate from './WeeklyUpdate';

const mapStateToProps = (state, ownProps) => {
  // tslint:disable-next-line:no-console
  console.log(state);
  // tslint:disable-next-line:no-console
  console.log(ownProps);
  const {[ownProps.season]: season} = state;
  // Gotta be a better way to do this w/ null coalesing? Tuple key?
  if(!season) {
    return {
      weekResults: null,
    };
  }
  const {[ownProps.round]: weekResults} = season;
  return {
    weekResults,
  }
};
   
const mapDispatchToProps = dispatch => bindActionCreators({
  getWeeklyUpdate,
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(WeeklyUpdate);
