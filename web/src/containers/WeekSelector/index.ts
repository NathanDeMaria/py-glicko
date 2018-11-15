import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { getSeasons } from 'src/actions/actionCreators';
import { IAppState } from 'src/interfaces';

import { IStateProps, WeekSelector } from './WeekSelector';

const mapStateToProps = (state: IAppState): IStateProps => {
  const {weekSelector} = state;
  return {
    seasons: weekSelector,
  };
};
   
const mapDispatchToProps = (dispatch: any) => bindActionCreators({
  getSeasons,
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(WeekSelector as any); // TODO: typescript better
