# Started on 29-Mar-2013; 9:40 PM, by mitthu
# The -( capsule )- project

import random

def reset_password_for_user(user):
	new_password = int(random.random()*10000000)

	user.set_password(new_password)
	user.save()

	sender = "Capsule Customer Support"
	subject = "Capsule password reset"
	message = "Dear %s,\n" % (user.username)
	message += "Your password has been reset to: %d. " % (new_password)
	message += "You are advised to change your password after your first login.\n\n"
	message += "Regards,\n"
	message += "The Capsule Team."

	user.email_user(subject, message, sender)
