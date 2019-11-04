import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { getSeasons } from 'src/actions/actionCreators';
import { IAppState } from 'src/interfaces';

import { IOwnProps, IStateProps, WeekSelector } from './WeekSelector';

const mapStateToProps = (state: IAppState, ownProps: IOwnProps): IStateProps => {
  const {weekSelector: {[ownProps.league]: seasons}} = state;
  if (seasons == null) {
    return {
      defaultWeeks: [],
      seasons,
    };
  }
  const lastSeason = Math.max(...Object.keys(seasons).map(s => parseInt(s, 10)));
  const defaultWeeks = seasons[lastSeason.toString()];
  return {
    defaultWeeks,
    seasons,
  };
};
   
const mapDispatchToProps = (dispatch: any) => bindActionCreators({
  getSeasons,
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(WeekSelector);
