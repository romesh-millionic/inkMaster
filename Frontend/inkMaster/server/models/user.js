const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');


const UserSchema = new mongoose.Schema({
  name: String,
  email: {
    type: String,
    index: { unique: true }
  },
  contact: String,
  password: String,
  role: String,
  type: String
});


UserSchema.methods.comparePassword = function comparePassword(password, callback) {
  bcrypt.compare(password, this.password, callback);
};


UserSchema.pre('save', function saveHook(next) {
  const user = this;

  if (!user.isModified('password')) return next();

  return bcrypt.genSalt((saltError, salt) => {
    if (saltError) { return next(saltError); }

    return bcrypt.hash(user.password, salt, (hashError, hash) => {
      if (hashError) { return next(hashError); }

      user.password = hash;

      return next();
    });
  });
});

module.exports = mongoose.model('User', UserSchema);
