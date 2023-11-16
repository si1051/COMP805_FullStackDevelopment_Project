import { combineReducers } from "redux";
import { userReducer } from "./UserReducer";
import { usersReducer } from './UsersReducer';

const rootReducer = combineReducers({
  user: userReducer,
  users: usersReducer,
});

export default rootReducer;
