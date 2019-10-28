import { connect } from 'react-redux';

import { IAppState } from 'src/interfaces';
import HistoryChart, { IOwnProps, IStateProps } from './HistoryChart';

const mapStateToProps = (state: IAppState, ownProps: IOwnProps): IStateProps => {
  const { league } = ownProps;
  const { teamHistory: {[league]: historiesObject = {}}} = state;
  return {
    histories: Object.keys(historiesObject).map(k => ({
      ratings: historiesObject[k],
      team: k,
    })),
  };
};

export default connect(mapStateToProps)(HistoryChart);
