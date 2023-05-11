import numpy as np

class QLearningAgent:
    def __init__(self, alpha, gamma, epsilon, get_state, actions):
        self.alpha = alpha # tasa de aprendizaje
        self.gamma = gamma # factor de descuento
        self.epsilon = epsilon # probabilidad de tomar una acción aleatoria
        self.get_state = get_state # función para obtener el estado actual
        self.actions = actions # lista de acciones posibles
        self.q = {} # diccionario que mapea estados a valores Q
        
    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(self.actions)
        else:
            q_vals = np.array([self.get_q(state, a) for a in self.actions])
            max_q = np.max(q_vals)
            if np.sum(q_vals == max_q) > 1:
                # hay varias acciones con el valor Q máximo, selecciona una al azar
                best_actions = [i for i in range(len(self.actions)) if q_vals[i] == max_q]
                action = self.actions[np.random.choice(best_actions)]
            else:
                action = self.actions[np.argmax(q_vals)]
        return action
        
    def get_q(self, state, action):
        if (state, action) not in self.q:
            self.q[(state, action)] = 0.0
        return self.q[(state, action)]
    
    def update_q(self, state, action, reward, next_state):
        old_value = self.get_q(state, action)
        next_max = np.max([self.get_q(next_state, a) for a in self.actions])
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q[(state, action)] = new_value
