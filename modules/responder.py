"""
Copyright 2014 Magnus Briden

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# encoding: UTF-8
import os, sys
from core.events import ReloadconfigEvent, RequestSendPrivmsgEvent, ReginfoEvent, ParsedPrivmsgEvent
from core.weakboundmethod import WeakBoundMethod as Wbm

class responder():
    def __init__(self, ed):
        self.ed = ed
        self.respond = False
        self.what = ""
        self._connections = [
            self.ed.add(ReloadconfigEvent, Wbm(self.config)),
            self.ed.add(ReginfoEvent, Wbm(self.module)),
            self.ed.add(ParsedPrivmsgEvent, Wbm(self.respond_method))
        ]
        
        
    def respond_method(self, event):
        nick, source = event.nick, event.source
        channel, message = event.channel, event.message
        command, parameters = event.command, event.parameters
        
        if self.respond:
            RequestSendPrivmsgEvent(nick, self.what).post(self.ed)
        
    
    def config(self, event):
        if event.module == "modules":
            RequestSendPrivmsgEvent(event.master, "Configurations reloaded, master!").post(self.ed)
        elif event.module == "responder":
            self.respond ^= True
            text = ""
            for word in event.master:
                text += "%s " % (word, )
            self.what = text.strip()
        
    def module(self, event):
        pass
        #if event.message != "modulereload":
        #   return
        #self.ed.post(SendPrivmsgEvent(event.master, "Modules reloaded, master!"))
