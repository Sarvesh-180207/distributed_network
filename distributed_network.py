
from collections import deque
from datetime import datetime


class Message:
    def __init__(self, sender, receiver, content, kind):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.kind = kind
        self.timestamp = datetime.now().strftime("%H:%M:%S")


class Node:
    def __init__(self, name):
        self.name = name
        self.inbox = deque()

    def send(self, receiver, content, kind="UNICAST"):
        message = Message(self.name, receiver.name, content, kind)
        receiver.inbox.append(message)

        print(f"\n[{kind}] {self.name} -> {receiver.name}")
        print(f"Message: {content}")
        print(f"Time: {message.timestamp}")

    def receive(self):
        if not self.inbox:
            print(f"\n{self.name}: No messages in inbox.")
            return None

        message = self.inbox.popleft()
        print(f"\n{self.name} received a message")
        print(f"From: {message.sender}")
        print(f"Type: {message.kind}")
        print(f"Content: {message.content}")
        return message


class DistributedNetwork:
    def __init__(self):
        self.nodes = {
            name: Node(name)
            for name in ["A", "B", "C", "D"]
        }

    def show_nodes(self):
        print("\nAvailable nodes:", ", ".join(self.nodes))

    def unicast(self):
        self.show_nodes()
        sender_name = input("Sender node: ").upper()
        receiver_name = input("Receiver node: ").upper()

        if sender_name not in self.nodes or receiver_name not in self.nodes:
            print("Invalid node name.")
            return

        if sender_name == receiver_name:
            print("Choose two different nodes.")
            return

        content = input("Enter message: ")
        self.nodes[sender_name].send(
            self.nodes[receiver_name], content
        )

    def broadcast(self):
        self.show_nodes()
        sender_name = input("Sender node: ").upper()

        if sender_name not in self.nodes:
            print("Invalid node name.")
            return

        content = input("Broadcast message: ")
        sender = self.nodes[sender_name]

        for name, receiver in self.nodes.items():
            if name != sender_name:
                sender.send(receiver, content, "BROADCAST")

    def multicast(self):
        self.show_nodes()
        sender_name = input("Sender node: ").upper()

        if sender_name not in self.nodes:
            print("Invalid sender.")
            return

        targets = input(
            "Enter receiver nodes separated by commas: "
        ).upper().split(",")

        targets = [target.strip() for target in targets]

        if (not targets
                or any(target not in self.nodes for target in targets)
                or sender_name in targets
                or len(set(targets)) != len(targets)):
            print("Invalid receiver group.")
            return

        content = input("Multicast message: ")
        sender = self.nodes[sender_name]

        for target in targets:
            sender.send(
                self.nodes[target], content, "MULTICAST"
            )

    def request_reply(self):
        self.show_nodes()
        sender_name = input("Requesting node: ").upper()
        receiver_name = input("Service node: ").upper()

        if (sender_name not in self.nodes
                or receiver_name not in self.nodes
                or sender_name == receiver_name):
            print("Choose two different valid nodes.")
            return

        sender = self.nodes[sender_name]
        receiver = self.nodes[receiver_name]

        request = input("Enter request: ")
        sender.send(receiver, request, "REQUEST")
        received = receiver.receive()

        if received:
            reply = "Reply to your request: " + received.content
            receiver.send(sender, reply, "REPLY")
            sender.receive()

    def receive_message(self):
        self.show_nodes()
        name = input("Node to receive messages: ").upper()

        if name in self.nodes:
            self.nodes[name].receive()
        else:
            print("Invalid node name.")

    def show_inboxes(self):
        print("\n--- INBOX STATUS ---")
        for name, node in self.nodes.items():
            print(f"\nNode {name}: {len(node.inbox)} message(s)")
            for message in node.inbox:
                print(
                    f"  From {message.sender}: {message.content}"
                )

    def run(self):
        while True:
            print("\n================================")
            print(" DISTRIBUTED COMMUNICATION MODEL")
            print("================================")
            print("1. Unicast (one-to-one)")
            print("2. Broadcast (one-to-all)")
            print("3. Multicast (one-to-selected-group)")
            print("4. Request and reply")
            print("5. Receive a message")
            print("6. View all inboxes")
            print("7. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.unicast()
            elif choice == "2":
                self.broadcast()
            elif choice == "3":
                self.multicast()
            elif choice == "4":
                self.request_reply()
            elif choice == "5":
                self.receive_message()
            elif choice == "6":
                self.show_inboxes()
            elif choice == "7":
                print("Network simulator stopped.")
                break
            else:
                print("Invalid choice. Enter a number from 1 to 7.")


if __name__ == "__main__":
    network = DistributedNetwork()
    network.run()
