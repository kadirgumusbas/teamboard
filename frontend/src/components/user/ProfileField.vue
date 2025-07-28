<script setup>
import { User, Mail, Calendar, Pencil } from "lucide-vue-next"
const props = defineProps({
  label: String,
  modelValue: String,
  readonly: { type: Boolean, default: false },
  editing: Boolean,
  icon: String,
})
const emit = defineEmits(['update:modelValue', 'edit', 'cancel', 'save'])

const iconMap = {
  user: User,
  mail: Mail,
  calendar: Calendar,
  pencil: Pencil,
}
const IconComponent = iconMap[props.icon] || User
</script>

<template>
  <div class="flex items-center gap-4">
    <!-- Icon -->
    <span class="shrink-0">
      <IconComponent class="w-5 h-5 text-gray-500" />
    </span>
    <span class="w-36 font-medium text-gray-700 dark:text-gray-200">{{ label }}:</span>
    <template v-if="readonly">
      <span class="text-gray-800 dark:text-gray-100">{{ modelValue }}</span>
    </template>
    <template v-else>
      <input
        v-if="editing"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        class="flex-1 px-2 py-1 rounded border border-gray-300 focus:ring focus:ring-gray-800 outline-none dark:bg-gray-900 dark:text-gray-100"
      />
      <span v-else class="flex-1 text-gray-800 dark:text-gray-100">{{ modelValue }}</span>
    </template>
    <template v-if="!readonly">
      <button v-if="!editing" @click="$emit('edit')" class="ml-2 text-gray-400 hover:text-blue-600">
        <Pencil class="w-4 h-4" />
      </button>
      <template v-else>
        <button @click="$emit('save')" class="ml-2 text-green-600 hover:text-green-800">Save</button>
        <button @click="$emit('cancel')" class="ml-2 text-gray-400 hover:text-red-600">Cancel</button>
      </template>
    </template>
  </div>
</template>
