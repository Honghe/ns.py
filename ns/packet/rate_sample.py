class RateSample:
    """
    The class rate sample used for estimation of delivery rate
    Y. Cheng, N. Cardwell, S. Hassas Yeganeh, V.Jacvobson 
    draft-cheng-iccrg-delivery-rate-estimation-02
    """
    def __init__(self):
        self.delivery_rate = 0
        self.delivered = 0
        self.prior_delivered = 0
        self.prior_time = 0
        self.newly_acked = 0
        self.last_acked = 0
        self.delivery_rate = 0
        self.send_rate = 0
        self.ack_rate = 0
        self.interval = 0
        self.ack_elapsed = 0
        self.send_elapsed = 0
        self.minRTT = -1
        
    def send_packet(packet, C, packets_in_flight, current_time):
        if (packets_in_flight == 0):
            C.first_sent_time = C.delivered_time = current_time
        packet.first_sent_time = C.first_sent_time
        packet.delivered_time = C.delivered_time
        # packet.delivered = C.delivered
        # packet.is_app_limited = (C.is_app_limited != 0)
        
    def updaterate_sample(self, packet, C ,current_time):
        if packet.delivered_time == 0:
            return # packet already sacked
        C.delivered += packet.size
        C.delivered_time = current_time

        if (packet.delivered < self.prior_delivered):
            self.prior_delivered = packet.delivered
            self.prior_time = packet.delivered_time
            self.is_app_limited = packet.is_app_limited
            self.send_elapsed = packet.sent_time - packet.first_sent_time
            self.ack_elapsed = C.delivered_time - packet.delivered_time
            C.first_sent_time = packet.sent_time
        
        packet.delivered_time = 0

    def update_sample_group(self, C, minRTT = -1):
        if(C.is_app_limited and C.delivered > C.is_app_limited):
                C.is_app_limited = 0
        if(self.prior_time == 0): 
            if(minRTT>0):
                if (self.minRTT == -1):
                    self.minRTT = minRTT
                self.minRTT = min(self.minRTT, minRTT)
            return False
        self.delivered = self.newly_acked = C.delivered - self.prior_delivered 
        self.interval = max(self.ack_elapsed, self.send_elapsed)
        if(self.interval < self.minRTT):
            self.interval = -1
            return False
        if(self.interval > 0):
            self.delivery_rate = self.delivered / self.interval
        if(minRTT>0):
            if (self.minRTT == -1):
                self.minRTT = minRTT
            self.minRTT = min(self.minRTT, minRTT)
        return True

class Connection:
    def __init__(self):
        self.is_app_limited = 0
        self.first_sent_time = 0
        self.delivered = 0
        self.delivered_time = 0

        
        