from openai import OpenAI
import time
import sys

client = OpenAI()

assistant_name=None
module_name=None
assistant_created=False

if assistant_name is None:
	assistant_name = str(sys.argv[1])

if module_name is None:
	module_name = "gpt-4-1106-preview"

# if assistant exists, use it
assistants_list = client.beta.assistants.list()
for existing_assistant in assistants_list.data:
	if existing_assistant.name == assistant_name:
		print("setup_assistant: using existing assistant: " + existing_assistant.name + " id:" + existing_assistant.id)
		assistant = client.beta.assistants.retrieve(existing_assistant.id)
		assistant_created = True

if assistant_created == False:
	assistant = client.beta.assistants.create(
		name = assistant_name,
		instructions = "You are a math tutor. Write and run code to answer math questions",
		tools = [{"type": "code_interpreter"}],
		model = "gpt-4-1106-preview"
	)
	print("Assistant " + assistant_name + " was created")

#run = client.beta.threads.runs.create(
#		thread_id = thread.id,
#		assistant_id = assistant.id
#		)


thread = client.beta.threads.create()
#print(thread)

message = client.beta.threads.messages.create(
		thread_id = thread.id,
		role = "user",
		content = "Solve the problem: 3x + 11 = 14"
	)

run = client.beta.threads.runs.create(
		thread_id = thread.id,
		assistant_id = assistant.id
		)

run = client.beta.threads.runs.retrieve(
		thread_id = thread.id,
		run_id = run.id
	)

# Wait for completion
while run.status != "completed":
	# Be nice to the API
	time.sleep(0.5)
	run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

try:
	messages = client.beta.threads.messages.list(
			thread_id = thread.id
		)
except:
	print("message list failed")
	exit()

#time.sleep(10)


for message in reversed(messages.data):
	print(message.role + ": " + message.content[0].text.value)