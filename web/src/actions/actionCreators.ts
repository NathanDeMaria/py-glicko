import { SUCCESS_GET_WEEKLY_UPDATE } from './actionTypes';

interface IUpdate {
  payload: any,
  type: string,
};

export const getWeeklyUpdate = (update: IUpdate) => ({
  payload: [{team: "Nebraska Cornhuskers", rating: 2000, variance:1 }],
  type: SUCCESS_GET_WEEKLY_UPDATE,
});
